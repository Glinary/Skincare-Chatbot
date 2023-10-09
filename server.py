# TODO: Fix routing of webhooks
# TODO: Diagnosis logic
# TODO: Update persistent menu

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
from messengerapi.components import Elements, Element, Buttons, Button, POSTBACK, PersistentMenu
from messengerapi.messenger_profile_api import ProfileApi

# ---------- LIBRARIES FOR GLITCH, FLASK, &MESSENGER API ---------- #

# imports the private keys from .env file
load_dotenv()
VERIFICATION_TOKEN = os.getenv('VERIFICATION_TOKEN')
PAGE_ACCESS_TOKEN = os.getenv('PAGE_ACCESS_TOKEN')

app = Flask(__name__)
send_api = SendApi(PAGE_ACCESS_TOKEN)
profile_api = ProfileApi(PAGE_ACCESS_TOKEN)

options_dict = {
  'option1': None,
  'option2': None,
  'option3': None,
  'option4': None,
  'option5': None
}

@app.route('/', methods=['GET'])
# Webhook validation
def verify():
  if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
    # Check if the verification token matches
    if not request.args.get("hub.verify_token") == VERIFICATION_TOKEN:
      return "Verification token mismatch", 403
    return request.args["hub.challenge"], 200
  
  print("You are on verify()")
  display_welcome_screen()
  return "The server is active 🤠", 200

def display_welcome_screen():
  buttons = Buttons()
  options = ["Diagnose skin", "Coming Soon"]
  
  welcome_message = "Hello! I am the Scire Technology Bot. If you'd like me to assess your skin type, enter 'Diagnose skin'."
  #confirm if this part works
  profile_api.set_welcome_screen(get_started_button_payload="<postback_payload>", greetings=[{"locale": "default", "text": welcome_message}])
  for option in options:
    button = Button(button_type=POSTBACK, title=option)
    buttons.add_button(button.get_content())
  persistentMenu = PersistentMenu(default_locale_menu=buttons.get_content())
  profile_api.set_persistent_menu(persistent_menu=persistentMenu.get_content())
  
  
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
        #send_menu(sender_id)
        
        answer = get_answer()
        if (answer == 'Diagnose skin'):
          return redirect(url_for('get_q_one', sender_id=sender_id))
        
        if ('postback' in messaging_event):
          payload = messaging_event['postback']['payload']
          title = messaging_event['postback']['title']
          if (payload == 'q_one'):
            options_dict['option1'] = title
            return post_q_one(sender_id, title)
          elif (payload == 'q_two'):
            options_dict['option2'] = title
            return post_q_two(sender_id, title)
          elif (payload == 'q_three'):
            options_dict['option3'] = title
            return post_q_three(sender_id, title)
          elif (payload == 'q_four'):
            options_dict['option4'] = title
            return post_q_four(sender_id, title)
          elif (payload == 'q_five'):
            options_dict['option5'] = title
            return post_q_five(sender_id, title)
          elif (payload == 'assessment'):
            return redirect(url_for('get_q_one', sender_id=sender_id))
  
  return 'OK', 200

@app.route('/get_q_one', methods=['GET'])
def get_q_one():
  print("You are on get_q_one()")
  sender_id = request.args.get("sender_id")
  elements = Elements()
  buttons1 = Buttons()
  buttons2 = Buttons()
  bot_response1 = "Great! I will ask you a series of questions, please answer as truthfully as you can."
  bot_response2 = """
  If you wash your face and don't apply any products, how does your skin behave 30 minutes after?\n
  A. It feels dry
  B. It feels calm, smooth, and soft
  C. It feels uneven (oily in some parts and dry on the other parts)
  D. It feels shiny and oily
  """
  bot_prompt = "Choose an answer"
  instructions = "Scroll left/right for more options"
  options1 = ['A', 'B']
  options2 = ['C', 'D']
  
  send_api.send_text_message(bot_response1, sender_id)
  send_api.send_text_message(bot_response2, sender_id)
  for option in options1:
    button = Button(button_type=POSTBACK, title=option)
    button.set_payload(payload='q_one')
    buttons1.add_button(button.get_content())
  for option in options2:
    button = Button(button_type=POSTBACK, title=option)
    button.set_payload(payload='q_one')
    buttons2.add_button(button.get_content())
  element1 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons1.get_content())
  element2 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons2.get_content())
  elements.add_element(element1.get_content())
  elements.add_element(element2.get_content())
  send_api.send_generic_message(elements.get_content(), sender_id)
  
  return 'OK', 200

#temporarily set like this since I haven't figured out how to trigger POST
#@app.route('/post_q_one', methods=['POST'])
def post_q_one(sender_id, option):
  print("You are on post_q_one()")
  sender_id = sender_id
  option = option
  
  print("I got option:", option)
  
  return redirect(url_for('get_q_two', sender_id=sender_id))

@app.route('/get_q_two', methods=['GET'])
def get_q_two():
  print("You are on get_q_two()")
  sender_id = request.args.get("sender_id")
  elements = Elements()
  buttons1 = Buttons()
  buttons2 = Buttons()
  buttons3 = Buttons()
  bot_response1 = """What does your skin typically look like at the end of the day?\n
  A. My forehead and nose are very shiny and oily but my cheeks are matte.
  B. Crazy oily.
  C. Tight or splotchy. Like the desert. I need to put moisturizer on ASAP!
  D. Dull and tired. It feels mostly dry.
  E. My complexion is only slightly oily at the end of the day.
  F. I have some redness and irritation when exposed to skincare products or other environmental factors.
  G. It looks normal. Not overly dry or oily.
  """
  bot_prompt = "Choose an answer"
  instructions = "Scroll left/right for more options"
  options1 = ['A', 'B', 'C']
  options2 = ['D', 'E', 'F']
  options3 = ['G']
  
  send_api.send_text_message(bot_response1, sender_id)
  for option in options1:
    button = Button(button_type=POSTBACK, title=option)
    button.set_payload(payload='q_two')
    buttons1.add_button(button.get_content())
  for option in options2:
    button = Button(button_type=POSTBACK, title=option)
    button.set_payload(payload='q_two')
    buttons2.add_button(button.get_content())
  for option in options3:
    button = Button(button_type=POSTBACK, title=option)
    button.set_payload(payload='q_two')
    buttons3.add_button(button.get_content())
  element1 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons1.get_content())
  element2 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons2.get_content())
  element3 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons3.get_content())
  elements.add_element(element1.get_content())
  elements.add_element(element2.get_content())
  elements.add_element(element3.get_content())
  send_api.send_generic_message(elements.get_content(), sender_id)  
  
  return 'OK', 200

def post_q_two(sender_id, option):
  print("You are on post_q_two()")
  sender_id = sender_id
  option = option
  print("I got option:", option)
  
  return redirect(url_for('get_q_three', sender_id=sender_id))

@app.route('/get_q_three', methods=['GET'])
def get_q_three():
  print("You are on get_q_two()")
  sender_id = request.args.get("sender_id")
  elements = Elements()
  buttons1 = Buttons()
  buttons2 = Buttons()
  bot_response1 = """Describe your pores.\n
  A. My pores are large, visible, and sometimes clogged all over my face.
  B. Depends on where they are on my face. My pores are medium to large around my T-zone.
  C. Small to medium-sized. My pores are small and not visible.
  D. They seem to change with the day. My pores are visible but small.
  """
  bot_prompt = "Choose an answer"
  instructions = "Scroll left/right for more options"
  options1 = ['A', 'B']
  options2 = ['C', 'D']
  
  send_api.send_text_message(bot_response1, sender_id)
  for option in options1:
    button = Button(button_type=POSTBACK, title=option)
    button.set_payload(payload='q_three')
    buttons1.add_button(button.get_content())
  for option in options2:
    button = Button(button_type=POSTBACK, title=option)
    button.set_payload(payload='q_three')
    buttons2.add_button(button.get_content())
  element1 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons1.get_content())
  element2 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons2.get_content())
  elements.add_element(element1.get_content())
  elements.add_element(element2.get_content())
  send_api.send_generic_message(elements.get_content(), sender_id)  
  
  return 'OK', 200

def post_q_three(sender_id, option):
  print("You are on post_q_three()")
  sender_id = sender_id
  option = option
  print("I got option:", option)
  
  return redirect(url_for('get_q_four', sender_id=sender_id))

@app.route('/get_q_four', methods=['GET'])
def get_q_four():
  print("You are on get_q_four()")
  sender_id = request.args.get("sender_id")
  elements = Elements()
  buttons1 = Buttons()
  bot_response1 = "How frequently do you have breakouts or active acne lesions?"
  bot_prompt = "Choose an answer"
  instructions = ""
  options1 = ['Frequent', 'Seldom']
  
  send_api.send_text_message(bot_response1, sender_id)
  for option in options1:
    button = Button(button_type=POSTBACK, title=option)
    button.set_payload(payload='q_four')
    buttons1.add_button(button.get_content())
  element1 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons1.get_content())
  elements.add_element(element1.get_content())
  send_api.send_generic_message(elements.get_content(), sender_id)  
  
  return 'OK', 200

def post_q_four(sender_id, option):
  print("You are on post_q_four()")
  sender_id = sender_id
  option = option
  print("I got option:", option)
  
  return redirect(url_for('get_q_five', sender_id=sender_id))
  
@app.route('/get_q_five', methods=['GET'])
def get_q_five():
  print("You are on get_q_four()")
  
  sender_id = request.args.get("sender_id")
  elements = Elements()
  buttons1 = Buttons()
  bot_response1 = "Have you ever had a sunburn or noticed pigmentation changes after sun exposure?"
  bot_prompt = "Choose an answer"
  instructions = ""
  options1 = ['Yes', 'No']
  
  send_api.send_text_message(bot_response1, sender_id)
  for option in options1:
    button = Button(button_type=POSTBACK, title=option)
    button.set_payload(payload='q_five')
    buttons1.add_button(button.get_content())
  element1 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons1.get_content())
  elements.add_element(element1.get_content())
  send_api.send_generic_message(elements.get_content(), sender_id)  
  
  return 'OK', 200

def post_q_five(sender_id, option):
  print("You are on post_q_five()")
  
  option1 = options_dict['option1']
  option2 = options_dict['option2']
  option3 = options_dict['option3']
  option4 = options_dict['option4']
  option5 = options_dict['option5']
  skin_type, acne_prone, sun_sensitive = '', '', ''
  print("options are:", option1, option2, option3, option4, option5)
  
  if (option1 == 'A'):
    if (option2 == 'C' or option2 == 'D'):
      skin_type = 'Dry'
    elif (option2 == 'G'):
      skin_type = 'Normal'
    elif (option2 == 'A' or option2 == 'B' or option2 == 'E'):
      print("COMBINATION SKIN TYPE")
      skin_type = 'Combination'
    elif (option2 == 'F'):
      skin_type = 'Sensitive'
  elif (option1 == 'B'):
    if (option2 == 'B'):
      if (option3 == 'A'):
        skin_type = 'Oily'
      else:
        skin_type = 'Normal'
    elif (option2 == 'C' or option2 == 'D'):
      if (option3 == 'B'):
        skin_type = 'Combination'
      else:
        skin_type = 'Dry'
    elif (option2 == 'A' or option2 == 'E'):
      skin_type = 'Combination'
    elif (option2 == 'F'):
      skin_type = 'Sensitive'
  elif(option1 == 'C'):
    if (option2 == 'F'):
      skin_type == 'Sensitive'
    elif (option2 == 'B'):
      if (option3 == 'A' or option3 == 'B'):
        skin_type = 'Oily'
      elif (option3 == 'C' or option3 == 'D'):
        skin_type = 'Combination'
      else:
        skin_type = 'Combination'
  elif (option1 == 'D'):
    if (option2 == 'F'):
      skin_type = 'Sensitive'
    elif (option2 == 'A' or option2 == 'E'):
      skin_type = 'Combination'
    elif (option2 == 'G'):
      if (option3 == 'A' or option3 == 'B'):
        skin_type = "Oily"
      else:
        skin_type = "Combination"
    else:
        skin_type = 'Oily'
        
  if (option4 == 'Frequent'):
    acne_prone = "Acne Prone"
  else:
    acne_prone = "Not Acne Prone"
    
  if (option5 == 'Yes'):
    sun_sensitive = "Sun Sensitive"
  else:
    sun_sensitive = "Not Sun Sensitive"
    
  print("I got option:", option)
  
  return redirect(url_for('get_assessment', sender_id=sender_id, skin_type=skin_type, acne_prone=acne_prone, sun_sensitive=sun_sensitive))

@app.route('/get_assessment', methods=['GET'])
def get_assessment():
  print("You are on get_assessment()")
  sender_id = request.args.get("sender_id")
  skin_type = request.args.get("skin_type")
  acne_prone = request.args.get("acne_prone")
  sun_sensitive = request.args.get("sun_sensitive")
  elements = Elements()
  buttons1 = Buttons()
  
  bot_response1 = f"""
  Diagnosis:
  Skin type: {skin_type}
  Acne Prone: {acne_prone}
  Sun Sensitive: {sun_sensitive}
  """
  bot_prompt = "Would you like to take the test again?"
  instructions = ""
  options1 = ['Diagnose my skin again']
  
  send_api.send_text_message(bot_response1, sender_id)
  for option in options1:
    button = Button(button_type=POSTBACK, title=option)
    button.set_payload(payload='assessment')
    buttons1.add_button(button.get_content())
  element1 = Element(title=bot_prompt, subtitle=instructions, image_url="", buttons=buttons1.get_content())
  elements.add_element(element1.get_content())
  send_api.send_generic_message(elements.get_content(), sender_id)  
  
  return 'OK', 200

def get_answer():
  data = request.get_json()
  #pprint(data)
  print("You are on get_answer()")
    
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
  send_api.send_generic_message(elements.get_content(), sender_id)
  
  return "OK", 200

def error_message(sender_id):
  send_api.send_text_message("Sorry, I didn't get that. Please try again.", sender_id)

if __name__ == "__main__":
	app.run(debug=True)
  
  
  


