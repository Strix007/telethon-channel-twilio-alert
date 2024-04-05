#!/usr/bin/env python

# Imports
from telethon import TelegramClient, events
from configparser import ConfigParser
from twilio.rest import Client

# Remove Traceback on KeyboardInterrupt
import signal
import os
signal.signal(signal.SIGINT, lambda x, y: os._exit(0))

# Parse config from config.cfg
config = ConfigParser()
config.read('config.cfg')

# Get user-specific variables from config.cfg
# Telegram
api_id = config.get('telethon', 'id')
api_hash = config.get('telethon', 'hash')
channel = config.get('telethon', 'channel')
# Keywords to include
keyword_include = config.get('telethon', 'include')
# Keywords to exclude
keyword_exclude = config.get('telethon', 'exclude')

# Twilio
account_SID = config.get('twilio', 'SID')
account_token = config.get('twilio', 'token')
twilioPh = config.get('twilio', 'twilioNo')
sendTo = config.get('twilio', 'send')
messageSent = config.get('twilio', 'message')

# Create a TelegramClient object
client = TelegramClient('my_account', api_id, api_hash)
# Create a TwilioClient object
twilioClient = Client(account_SID, account_token)

# Define an event handler for incoming messages in the channel
@client.on(events.NewMessage(chats=channel))
async def handle_new_message(event):
    message_text = event.message.text.lower()
    # Filter message accounting to keywords
    if keyword_include in message_text and keyword_exclude not in message_text:
        print(event.message.text)
        # Send a message to your phone number with the message recieved
        twilioClient.messages.create(
            body = messageSent + " " + event.message.text,
            from_=twilioPh,
            to=sendTo
        )

# Run the client
async def main():
    await client.start()
    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
