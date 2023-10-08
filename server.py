# TODO: Fix routing of webhooks
# TODO: Diagnosis logic

# ---------- DEPENDENCIES ---------- #
'pip install typing'
'pip install python-dotenv'
'pip install flask requests'
'pip3 install messenger-api-python'
# ---------- DEPENDENCIES ---------- #

# ---------- LIBRARIES FOR PRIVATE TOKENS ---------- #
from dotenv import load_dotenv
import os, sys

# ---------- LIBRARIES FOR PRIVATE TOKENS ---------- #
# ---------- LIBRARIES FOR GLITCH, FLASK, & MESSENGER API ---------- #
from flask import Flask, request, redirect, url_for
from pprint import pprint
from messengerapi import SendApi
from messengerapi.components import Elements, Element, Buttons, Button, POSTBACK
# ---------- LIBRARIES FOR GLITCH, FLASK, &MESSENGER API ---------- #

# imports the private keys from .env file
load_dotenv()
VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')

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
  
  return "The server is active 🤠", 200

@app.route('/get_q_one', methods=['GET'])
def get_q_one():
  sender_id = request.args.get('sender_id')
  q_one(sender_id)
            
  return "q_one done", 200

@app.route('/get_q_two', methods=['GET'])
def get_q_two():
  sender_id = request.args.get('sender_id')
  q_one(sender_id)
  
  answer = get_answer()
  if (answer):
    return redirect(url_for('get_q_two', sender_id=sender_id, skin_type=answer))
  return "q_two done", 200

@app.route('/get_q_three', methods=['GET'])
def get_q_three():
  sender_id = request.args.get('sender_id')
  q_one(sender_id)
  return "q_three done", 200

@app.route('/get_q_four', methods=['GET'])
def get_q_four():
  sender_id = request.args.get('sender_id')
  q_one(sender_id)
  return "q_four done", 200

@app.route('/get_q_five', methods=['GET'])
def get_q_five():
  sender_id = request.args.get('sender_id')
  q_one(sender_id)
  return "q_five done", 200
  
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
          send_menu(sender_id)
          
          # Handle a yes response
          answer = get_answer()
          if (answer == "Yes"):
            return redirect(url_for('get_q_one', sender_id=sender_id))
          elif (answer == "No"):
            send_api.send_text_message("That's okay! If you change your mind, I'm here to help")
            return "OK", 200
  
    return 'OK', 200
  
def get_answer():
  data = request.get_json()
  pprint(data)
    
  if data['object'] == 'page':
    for entry in data['entry']:
      for messaging_event in entry['messaging']:
        if 'postback' in messaging_event:
          message = messaging_event['postback']['title']
          print("message:", message)
          return message
        
  return "I didn't get an answer"
  
def send_menu(sender_id):
  elements = Elements()
  buttons = Buttons()
  bot_prompt = "Hi! I'm the Scire Technology Bot. Would you like me to assess your skin type?"
  instructions = "Choose an option"
  options = ["Yes", "No"]
  
  for option in options:
    button = Button(button_type=POSTBACK, title=option)
    buttons.add_button(button.get_content())
  element = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons.get_content())
  elements.add_element(element.get_content())
  send_api.send_generic_message(elements.get_content() , sender_id)
  
  return "OK", 200

def q_one(sender_id):
  elements = Elements()
  buttons1 = Buttons()
  buttons2 = Buttons()
  bot_prompt = "Choose an option"
  instructions = ""
  bot_response1 = "Great! I will ask you a series of questions, please answer as truthfully as you can."
  bot_response2 = """
  If you wash your face and don't apply any products, how does your skin behave 30 minutes after?\n
  A. It feels dry
  B. It feels calm, smooth, and soft
  C. It feels uneven (oily in some parts and dry on the other parts)
  D. It feels shiny and oily
  """
  options1 = ["A", "B"]
  options2 = ["C", "D"]
  
  send_api.send_text_message(bot_response1, sender_id)
  send_api.send_text_message(bot_response2, sender_id)
  
  for option in options1:
    button = Button(button_type=POSTBACK, title=option)
    buttons1.add_button(button.get_content())
  for option in options2:
    button = Button(button_type=POSTBACK, title=option)
    buttons2.add_button(button.get_content())
  element1 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons1.get_content())
  element2 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons2.get_content())
  
  elements.add_element(element1.get_content())
  elements.add_element(element2.get_content())

  send_api.send_generic_message(elements.get_content() , sender_id)
  
  return "OK", 200
  
def q_two(sender_id):
  bot_response = """
  What does your skin typically look like at the end of the day?\n
  A. My forehead and nose are very shiny and oily but my cheeks are matte.
  B. Crazy oily.
  C. Tight or splotchy. Like the desert. I need to put moisturizer on ASAP!
  D. Dull and tired. It feels mostly dry.
  E. My complexion is only slightly oily at the end of the day.
  F. I have some redness and irritation when exposed to skincare products or other environmental factors.
  G. It looks normal. Not overly dry or oily.
  """
  bot_prompt = "Choose an option"
  instructions = ""
  options1 = ["A", "B", "C"]
  options2 = ["D", "E"]
  options3 = ["F", "G"]
  elements = Elements()
  buttons1 = Buttons()
  buttons2 = Buttons()
  buttons3 = Buttons()
  
  send_api.send_text_message(bot_response, sender_id)
  for option in options1:
    button = Button(button_type=POSTBACK, title=option)
    buttons1.add_button(button.get_content())
  for option in options2:
    button = Button(button_type=POSTBACK, title=option)
    buttons2.add_button(button.get_content())
  for option in options3:
    button = Button(button_type=POSTBACK, title=option)
    buttons3.add_button(button.get_content())
  element1 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons1.get_content())
  element2 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons2.get_content())
  element3 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons3.get_content())
  elements.add_element(element1.get_content())
  elements.add_element(element2.get_content())
  elements.add_element(element3.get_content())
  send_api.send_generic_message(elements.get_content() , sender_id)
  
  return "OK", 200

def q_three(sender_id):
  bot_response = """
  Describe your pores\n
  A. My pores are large, visible, and sometimes clogged all over my face.
  B. Depends on where they are on my face. My pores are medium to large around my T-zone.
  C. Small to medium-sized. My pores are small and not visible.
  D. They seem to change with the day. My pores are visible but small.
  """
  bot_prompt = "Choose an option"
  instructions = ""
  options1 = ["A", "B"]
  options2 = ["C", "D"]
  
  send_api.send_text_message(bot_response, sender_id)
  elements = Elements()
  buttons1 = Buttons()
  buttons2 = Buttons()
  
  send_api.send_text_message(bot_response, sender_id)
  for option in options1:
    button = Button(button_type=POSTBACK, title=option)
    buttons1.add_button(button.get_content())
  for option in options2:
    button = Button(button_type=POSTBACK, title=option)
    buttons2.add_button(button.get_content())
  element1 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons1.get_content())
  element2 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons2.get_content())
  elements.add_element(element1.get_content())
  elements.add_element(element2.get_content())
  send_api.send_generic_message(elements.get_content() , sender_id)
  
  return "OK", 200
  
def q_four(sender_id):
  bot_prompt = "How frequently do you have breakouts or active acne lesions?"
  instructions = "Choose an option"
  options = ["Frequent", "Seldom"]
  
  elements = Elements()
  buttons = Buttons()
  
  for option in options:
    button = Button(button_type=POSTBACK, title=option)
    buttons.add_button(button.get_content())
  element = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons.get_content())
  elements.add_element(element.get_content())
  send_api.send_generic_message(elements.get_content() , sender_id)
  
  return "OK", 200

def q_five(sender_id):
  bot_prompt = "Have you ever had a sunburn or noticed pigmentation changes after sun exposure?"
  instructions = "Choose an option"
  options = ["Yes", "No"]
  
  elements = Elements()
  buttons = Buttons()
  
  for option in options:
    button = Button(button_type=POSTBACK, title=option)
    buttons.add_button(button.get_content())
  element = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons.get_content())
  elements.add_element(element.get_content())
  send_api.send_generic_message(elements.get_content() , sender_id)
  
  return "OK", 200

def get_assessment(skin_type, acne_prone, sun_sensitive, sender_id):
  send_api.send_text_message("Thank you, <name> for answering the questions!\nHere's your assessment:")
  send_api.send_text_message(f"""
  Skin Type: {skin_type}
  Acne Prone: {acne_prone}
  Sun-Sensitive: {sun_sensitive}\n
  
  If you have any more question or need further assistance, feel free to ask!
  """, sender_id)

  
def error_message(sender_id):
  send_api.send_text_message("Sorry, I didn't get that. Please try again.", sender_id)

if __name__ == "__main__":
	app.run(debug=True)
  


