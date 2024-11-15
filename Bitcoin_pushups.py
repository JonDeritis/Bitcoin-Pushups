import os
import cv2
import mediapipe as mp
import asyncio
import requests
import uuid
import time

# Strike API key
STRIKE_API_KEY = 'YOUR_STRIKE_API_KEY'

# Threshold for Bitcoin transaction
pushup_count = 0
threshold = 10
transaction_triggered = False  # Tracks if transaction has already occurred

# Pose detection setup
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

def create_currency_exchange_quote():
    """Create a currency exchange quote to convert USD to BTC."""
    idempotency_key = str(uuid.uuid4())  # Generate a unique idempotency key
    url = "https://api.strike.me/v1/currency-exchange-quotes"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {STRIKE_API_KEY}',
        'idempotency-key': idempotency_key
    }
    data = {
        "sell": "USD",
        "buy": "BTC",
        "amount": {
            "amount": "1.00",  # $1 USD to BTC exchange
            "currency": "USD"
        },
        "feePolicy": "INCLUSIVE"
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code in [200, 201]:
        print("Quote created successfully.")
        return response.json().get("id")
    else:
        print("Error creating quote:", response.text)
        return None

def execute_currency_exchange_quote(quote_id):
    """Execute the currency exchange quote."""
    url = f"https://api.strike.me/v1/currency-exchange-quotes/{quote_id}/execute"
    headers = {
        'Authorization': f'Bearer {STRIKE_API_KEY}',
        'Accept': 'application/json'
    }
    response = requests.patch(url, headers=headers)
    if response.status_code == 202:
        print("Transaction accepted and processing.")
        return response.headers.get("Location")  # Location for status check
    else:
        print("Error executing quote:", response.text)
        return None

def check_currency_exchange_status(location_url):
    """Check the status of a currency exchange."""
    headers = {
        'Authorization': f'Bearer {STRIKE_API_KEY}',
        'Accept': 'application/json'
    }
    response = requests.get(location_url, headers=headers)
    if response.status_code == 200:
        print("Currency exchange status:", response.json())
    else:
        print("Error checking status:", response.text)

def handle_currency_exchange():
    print("10 pushups completed! Initiating SMASH BUY...")

    # Step 1: Create the currency exchange quote
    quote_id = create_currency_exchange_quote()
    if quote_id:
        # Step 2: Execute the currency exchange quote
        location_url = execute_currency_exchange_quote(quote_id)
        if location_url:
            # Step 3: Check the status of the currency exchange
            check_currency_exchange_status(location_url)
        else:
            print("Failed to retrieve status URL.")
    else:
        print("Failed to create a currency exchange quote.")

async def pushup_detection():
    global pushup_count, transaction_triggered
    pushup_position = "up"
    show_message = False
    message_end_time = 0
    blink_on = True

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Process the frame for pose detection
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
            left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y
            right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y

            # Pushup detection logic
            if pushup_position == "up" and left_shoulder > left_elbow * 0.95 and right_shoulder > right_elbow * 0.95:
                pushup_position = "down"
            elif pushup_position == "down" and left_shoulder < left_elbow * 0.95 and right_shoulder < right_elbow * 0.95:
                pushup_count += 1
                pushup_position = "up"
                print(f"Pushup count: {pushup_count}")

                # Trigger transaction once at the first threshold
                if pushup_count == threshold and not transaction_triggered:
                    transaction_triggered = True
                    handle_currency_exchange()  # Run the currency exchange transaction
                    show_message = True
                    message_end_time = time.time() + 2  # Display message for 2 seconds

        # Display pushup count on the frame
        cv2.putText(frame, f'Pushup Count: {pushup_count}', (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 165, 255), 2, cv2.LINE_AA)

        # Show "You just smash bought Bitcoin!" message for a brief time with blinking effect
        if show_message:
            if time.time() < message_end_time:
                if blink_on:
                    cv2.putText(frame, "You just smash bought Bitcoin!", (10, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
                # Toggle blink effect every 0.3 seconds
                if int((time.time() * 10) % 6) == 0:
                    blink_on = not blink_on
            else:
                show_message = False  # Hide message after 2 seconds

        cv2.imshow('Pushup Counter', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run pushup detection asynchronously
if __name__ == "__main__":
    asyncio.run(pushup_detection())
