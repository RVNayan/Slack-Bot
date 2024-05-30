import os
import slack
import re
import csv
import requests
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from main import SlackChannelManager  # Import the SlackChannelManager class from main.py
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import time

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.getenv('SIGNING_SECRET'), '/slack/events', app)

# Initialize Slack WebClient with bot token
client = WebClient(token=os.getenv('BOT_TOKEN'))
BOT_ID = client.api_call("auth.test")['user_id']

# Initialize SlackChannelManager with user token
channel_manager = SlackChannelManager(token=os.getenv('USER_TOKEN'))

last_processed_time = 0

@slack_event_adapter.on('message')
def message(payload):
    global last_processed_time
    event = payload.get('event', {})
    post_channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text', '')
    current_time = time.time()

    # Check if the current message is within 5 seconds of the last processed message
    # if current_time - last_processed_time < 5:
    #     print("Message received within 5 seconds of the last one. Ignoring.")
    #     return

    # Update the timestamp of the last processed message
    last_processed_time = current_time

    # Your existing message processing code...

    # Function 1
    if BOT_ID != user_id:
    
        if ("remove_user" in text.lower() or "add_user" in text.lower()):
            user_match = re.search(r'<@(.*?)>', text)
            if user_match:
                user_to_modify = user_match.group(1)
                print("User ID:", user_to_modify)
                
                if user_to_modify != user_id and user_to_modify != BOT_ID:
                    channel_matches = re.findall(r'<#(.*?)\|', text)
                    if channel_matches:
                        channels = channel_matches
                        print("Channels:", channels)
                        
                        if "remove_user" in text.lower():
                            for channel_id in channels:
                                channel_manager.remove_user_from_channel(user_to_modify, channel_id)
                            client.chat_postMessage(channel=post_channel_id, text=f"User <@{user_to_modify}> removed from specified channels.")
                        elif "add_user" in text.lower():
                            for channel_id in channels:
                                channel_manager.add_user_to_channel(user_to_modify, channel_id)
                            client.chat_postMessage(channel=post_channel_id, text=f"User <@{user_to_modify}> added to specified channels.")
                    else:
                        client.chat_postMessage(channel=post_channel_id, text="No channels specified.")
                
                else:
                    client.chat_postMessage(channel=post_channel_id, text="Sorry you cannot enter your name!")
            else:
                client.chat_postMessage(channel=post_channel_id, text="User ID not found.")

        # Function 2
        elif ("get_channels" in text.lower()):
            username_match = re.search(r'<@(.*?)\>', text)
            if username_match:
                user_id = username_match.group(1)
                print(user_id)
                
                user_channels = channel_manager.find_user_channels(user_id)

                if user_channels:
                    message = f"User <@{user_id}> is present in these channels:\n" + "\n".join([f" #{channel}" for channel in user_channels])
                    client.chat_postMessage(channel=post_channel_id, text=message)

                    # Save user_channels data to CSV
                    csv_file = 'user_channels.csv'
                    with open(csv_file, mode='w', newline='') as file:
                        writer = csv.DictWriter(file, fieldnames=["user_id", "channel"])
                        writer.writeheader()
                        for channel in user_channels:
                            writer.writerow({"user_id": user_id, "channel": channel})

                    # Check if file is written correctly
                    if os.path.exists(csv_file):
                        print(f"CSV file {csv_file} written successfully.")

                        try:
                            # Step 1: Get upload URL
                            file_size = os.path.getsize(csv_file)
                            response = client.files_getUploadURLExternal(
                                filename=csv_file,
                                length=file_size
                            )
                            upload_url = response['upload_url']
                            file_id = response['file_id']

                            # Step 2: Upload file
                            with open(csv_file, 'rb') as f:
                                upload_response = requests.post(upload_url, files={'file': f})

                            if upload_response.status_code != 200:
                                raise Exception(f"Failed to upload file: {upload_response.text}")

                            # Step 3: Complete upload
                            complete_response = client.files_completeUploadExternal(
                                files=[{
                                    'id': file_id,
                                    'title': 'User Channels CSV'
                                }],
                                channel_id=post_channel_id
                            )

                            if complete_response['ok']:
                                client.chat_postMessage(
                                    channel=post_channel_id,
                                    text="Here's the CSV file with user channels data."
                                )
                            else:
                                raise Exception(f"Failed to complete upload: {complete_response['error']}")

                        except SlackApiError as e:
                            print(f"Error uploading file: {e.response['error']}")
                        except Exception as e:
                            print(f"Error during file upload process: {str(e)}")

                else:
                    message = f"User <@{user_id}> is not found in any channels (that the app has access to)."
                    client.chat_postMessage(channel=post_channel_id, text=message)
            else:
                message = "User mention not found in the message."
                client.chat_postMessage(channel=post_channel_id, text=message)

        elif ("get_channels" in text.lower() and 'remove_user' in text.lower() or "add_user" in text.lower()):
            client.chat_postMessage(channel=post_channel_id, text="Invalid Command")
            
    elif BOT_ID == user_id:
        print("Message is from the bot itself. Ignoring.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
