Bitcoin Pushup SMASH BUY

This project is a unique and fun way to convert USD to BTC using the Strike API—every 10 pushups, a transaction is initiated! 
The code leverages computer vision through a webcam to count pushups and performs a Bitcoin transaction once a specified threshold is reached.

Features

Real-Time Pushup Detection: Uses OpenCV and MediaPipe for webcam-based pushup tracking.
Automated Bitcoin Transaction: After hitting the pushup threshold, the Strike API initiates a USD-to-BTC conversion.
Customizable Threshold and Amount: Easily adjust the number of pushups required for a transaction and the USD amount to convert.

Requirements:
Python 3.x
API Key: A Strike API key is required for transactions.
Python Packages:
opencv-python
mediapipe
requests (for API calls)

To install dependencies:

Copy code:
pip install opencv-python mediapipe requests

Setup
1. Clone this repository

Copy code
git clone https://github.com/

Open
cd bitcoin-pushups

2. Set up your Strike API key

Obtain your Strike API key by registering at Strike.
Replace the placeholder YOUR_STRIKE_API_KEY in bitcoin_pushups.py with your API key.

3. Configure Settings

Threshold: Change the number of pushups required to trigger a transaction by updating the threshold variable.
Transaction Amount: Modify the amount in USD to convert to BTC by adjusting the "amount" field in the create_currency_exchange_quote() function.

Example Configuration

To change the pushup threshold:

threshold = 10  # Adjust the number here

To change the amount of USD converted:

"amount": {
    "amount": "1.00",  # Change "1.00" to the desired USD amount
    "currency": "USD"
}

Run the Script: Start the program, which will automatically open the webcam for real-time pushup detection.

Copy code
python bitcoin_pushups.py

Perform Pushups: 
Make sure you are facing the camera for the best results and keep the camera realitively low to have your arms in view. 
Do pushups until you reach the threshold. After the threshold is met, the program initiates a transaction through Strike.

View Confirmation: 
The screen will display a "You just smash bought Bitcoin!" message briefly after each transaction, and the program will continue counting pushups.

Optional
Adjust Display Message: The message can be customized by editing the text in cv2.putText() in the code.

Once the threshold is reached, you’ll see:

Pushup count: [number] for each pushup.
A message "You just smash bought Bitcoin!" on the screen for 2 seconds.

Troubleshooting

Invalid API Key: Ensure that you enter a valid Strike API key; otherwise, an "Unauthorized" error will occur.

Webcam Not Detected: If the program can’t access the webcam, verify the device permissions.

License
This project is open-source and available under the MIT License.

