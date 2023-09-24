# ---------- DEPENDENCIES ---------- #
'pip install typing'
'pip install python-dotenv'
'pip install flask requests'
'pip3 install messenger-api-python'
# ---------- DEPENDENCIES ---------- #

# ---------- LIBRARIES FOR PRIVATE TOKENS ---------- #
from typing import Final
from dotenv import load_dotenv
import os, sys

# ---------- LIBRARIES FOR PRIVATE TOKENS ---------- #
# ---------- LIBRARIES FOR GLITCH, FLASK, & MESSENGER API ---------- #
from flask import Flask, request, render_template, make_response   #ERIKA_ADDED
from pprint import pprint
from messengerapi import SendApi
# ---------- LIBRARIES FOR GLITCH, FLASK, &MESSENGER API ---------- #

# imports the private keys from .env file
load_dotenv()
VERIFICATION_TOKEN: Final = os.getenv('VERIFICATION_TOKEN')
PAGE_ACCESS_TOKEN: Final = os.getenv('PAGE_ACCESS_TOKEN')

app = Flask(__name__)
send_api = SendApi(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
# Webhook validation
def verify():
  if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
    # Check if the verification token matches
    if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
      return "Verification token mismatch", 403
    return request.args["hub.challenge"], 200
  # Render the HTML template
  html_content = render_template("verify.html")
  # Create a response object with both HTML content and a 200 status code
  response = make_response(html_content)
  response.status_code = 200
  
  return response

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    pprint(data)
    
    if data['object'] == 'page':
      for entry in data['entry']:
        for messaging_event in entry['messaging']:
          # Retrieve the sender id
          sender_id = messaging_event['sender']['id']
          # Send a message to sender
          send_api.send_text_message("hi there", sender_id)
    
    return 'OK', 200

if __name__ == "__main__":
	app.run(debug=True)
  


