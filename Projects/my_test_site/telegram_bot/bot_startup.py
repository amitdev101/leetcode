import telepot
from telepot.loop import MessageLoop
import time
import requests

BACKEND_SERVER = ''
CHAT_ID = 1
TOKEN = ''

def handle(msg):
    # Extracting content type, chat type, and chat ID from the incoming message.
    content_type, chat_type, chat_id = telepot.glance(msg)
    
    # Printing the user ID (or chat ID) and type of message to the console.
    print(f"User ID: {chat_id}, Message Type: {content_type}")
    if chat_id == CHAT_ID :
    # If the received content is text, echo it back to the sender with their user ID (or chat ID).
        if content_type == 'text':
            bot.sendMessage(chat_id, f"User ID: {chat_id}, You said: {msg['text']}")
            command_text = msg['text']
            # Send the command to Django backend
            response = requests.post(BACKEND_SERVER, data={'command_text': command_text})

            if response.json().get('status') == 'success':
                bot.sendMessage(chat_id, "Command received!")
            else:
                bot.sendMessage(chat_id, "Failed to process command.")


# Replace with your bot token obtained from BotFather.
bot = telepot.Bot(TOKEN)
# Initiating the message loop to keep listening for incoming messages.
MessageLoop(bot, handle).run_as_thread()
print('Bot is listening ...')
# Keeping the script running.
while True:
    time.sleep(10)
