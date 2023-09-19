# ---------- DEPENDENCIES ---------- #
'pip install typing'
'pip install python-dotenv'
'pip install fbchat'
# ---------- DEPENDENCIES ---------- #

# ---------- LIBRARIES FOR PRIVATE TOKENS ---------- #
from typing import Final
from dotenv import load_dotenv
import os
# ---------- LIBRARIES FOR PRIVATE KEYS ---------- #
# ---------- LIBRARIES FOR MESSENGER API ---------- #
from fbchat import log, Client
# ---------- LIBRARIES FOR MESSENGER API ---------- #

# imports the private keys from .env file
load_dotenv()
FB_EMAIL: Final = os.getenv('FB_EMAIL')
FB_PASSWORD: Final = os.getenv('FB_PASSWORD')

# Subclass fbchat.Client and override required methods
class EchoBot(Client):
    def onMessage(self, author_id, message_object, thread_id, thread_type, **kwargs):
        self.markAsDelivered(thread_id, message_object.uid)
        self.markAsRead(thread_id)

        log.info("{} from {} in {}".format(message_object, thread_id, thread_type.name))

        # If you're not the author, echo
        if author_id != self.uid:
            self.send(message_object, thread_id=thread_id, thread_type=thread_type)


client = EchoBot(FB_EMAIL, FB_PASSWORD)
client.listen()