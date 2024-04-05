#!/usr/bin/env python

# Imports
import os
import signal
from telethon import TelegramClient, events
from configparser import ConfigParser
from twilio.rest import Client

# Remove Traceback on KeyboardInterrupt
signal.signal(signal.SIGINT, lambda x, y: os._exit(0))

# Prompts user for config input if file doesn't exist; otherwise, skips input and informs user.
cfg_file_path = "config.cfg"
# Check if the configuration file exists
if not os.path.exists(cfg_file_path):
    # Define the template configuration file content with placeholders
    cfg_template = """
[telethon]
id = {id}
hash = {hash}
channel = {channel}
include = {include}
exclude = {exclude}

[twilio]
SID = {sid}
token = {token}
twilioNo = {twilioNo}
send = {send}
message = {message}
    """

    # Get user input for each configuration value
    id = input("Your Telegram API id: ")
    hash = input("Your Telegram API hash: ")
    channel = input("Paste the URL of the channel you want to monitor: ")
    include = input("Keyword you want to include in the recieved channel message: ")
    exclude = input("Keyword you want to exclude in the recieved channel message: ")
    sid = input("Your Twilio account SID: ")
    token = input("Your Twilio account token: ")
    twilioNo = input("Your Twilio account number: ")
    send = input("The number you want to send the message to with the country code: ")
    message = input("The message you want to send: ")

    # Replace placeholders in the template with user input
    cfg_content = cfg_template.format(id=id, hash=hash, channel=channel, include=include, exclude=exclude, sid=sid, token=token, twilioNo=twilioNo, send=send,message=message)

    # Write the configuration content to a cfg file
    with open("config.cfg", "w") as cfg_file:
        cfg_file.write(cfg_content)

    print("Configuration saved to 'config.cfg'")
else:
    print("Configuration file already exists. Skipping input prompts.")

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
