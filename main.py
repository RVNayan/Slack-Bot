
#Code to add or remove user
"""
To use it in the bot file, include the below code

from remove_user import SlackChannelManager
import os
from dotenv import load_dotenv
from pathlib import Path

if __name__ == "__main__":
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    user_token = os.getenv('USER_TOKEN')
    manager = SlackChannelManager(token=user_token)
    
    user_id = 'D073ZB8JA4X'
    channel_name = '02-trail'

    manager.remove_user_from_channel(user_id, channel_name)
    manager.add_user_to_channel(user_id, channel_name)

    
ngrok code in terminal ngrok http --domain=learning-clever-gibbon.ngrok-free.app 5000

"""
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from pathlib import Path
import csv


class SlackChannelManager:
    def __init__(self, token):
        self.client = WebClient(token=token)

    def remove_user_from_channel(self, user_id, channel_name):
        try:

            response = self.client.conversations_list(types='public_channel,private_channel')
            channels = response['channels']
            
            # Print all channels for debugging
            print("Channels found:")
            for channel in channels:
                print(f"Name: {channel['name']}, ID: {channel['id']}")
            ################################## Can be commented
            channel_id = None
            for channel in channels:
                if channel['id'] == channel_name:
                    channel_id = channel['id']
                    break
            
            if channel_id:
                print(f"Attempting to remove user {user_id} from channel {channel_name} (ID: {channel_id})")

                # Check if the user is a member of the channel
                try:
                    response = self.client.conversations_members(channel=channel_id)
                    members = response['members']
                    if user_id in members:
                        try:
                            self.client.conversations_kick(channel=channel_id, user=user_id)
                            print(f"User {user_id} removed from channel: {channel_name}")
                        except SlackApiError as e:
                            print(f"Error removing user from channel '{channel_name}': {e.response['error']}")
                    else:
                        print(f"User {user_id} is not a member of the channel '{channel_name}'")

                except SlackApiError as e:
                    print(f"Error checking members of the channel '{channel_name}': {e.response['error']}")
            else:
                print(f"Channel '{channel_name}' not found")

        except SlackApiError as e:
            print(f"Error retrieving channels: {e.response['error']}")


    #Add people to channel

    def add_user_to_channel(self, user_id, channel_name):
        try:
            # Find the channel ID by its name
            response = self.client.conversations_list(types='public_channel,private_channel')
            channels = response['channels']
            
            # Print all channels for debugging
            print("Channels found:")
            for channel in channels:
                print(f"Name: {channel['name']}, ID: {channel['id']}")

            channel_id = None
            for channel in channels:
                if channel['id'] == channel_name:
                    channel_id = channel['id']
                    break
            
            if channel_id:
                print(f"Attempting to add user {user_id} to channel {channel_name} (ID: {channel_id})")
                
                try:
                    self.client.conversations_invite(channel=channel_id, users=user_id)
                    print(f"User {user_id} added to channel: {channel_name}")
                except SlackApiError as e:
                    print(f"Error adding user to channel '{channel_name}': {e.response['error']}")
            else:
                print(f"Channel '{channel_name}' not found")

        except SlackApiError as e:
            print(f"Error retrieving channels: {e.response['error']}")



    # def get_channels(self):
        
    #     channels = []
    #     seen_channel_ids = set()
    #     cursor = None

    #     try:
    #         while True:
    #             if cursor:
    #                 response = self.client.conversations_list(types="public_channel,private_channel", cursor=cursor)
    #             else:
    #                 response = self.client.conversations_list(types="public_channel,private_channel")

    #             if response["ok"]:
    #                 for channel in response["channels"]:
    #                     if channel["id"] not in seen_channel_ids:
    #                         channels.append(channel)
    #                         seen_channel_ids.add(channel["id"])

    #                 cursor = response.get("response_metadata", {}).get("next_cursor")

    #                 # Break the loop if there are no more pages
    #                 if not cursor:
    #                     break
    #             else:
    #                 print(f"Error fetching channels: {response['error']}")
    #                 break
    #     except SlackApiError as e:
    #         print(f"Slack API Error: {e.response['error']}")

    #     return channels

    def get_channels(self):
        channels = []
        seen_channel_ids = set()
        csv_file = 'channels.csv'

        # Read channels from the CSV file
        try:
            with open(csv_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row["id"] not in seen_channel_ids:
                        channels.append({"id": row["id"], "name": row["name"]})
                        seen_channel_ids.add(row["id"])
        except FileNotFoundError:
            print(f"CSV file {csv_file} not found. Please run all_channels() to generate the file.")
        
        return channels

    def get_user_id(self,username):
        try:
            response = self.client.users_list()
            if response["ok"]:
                for user in response["members"]:
                    if user["profile"]["real_name"] == username:
                        return user["id"]
            print(f"User {username} not found.")
            return None
        except SlackApiError as e:
            print(f"Slack API Error: {e.response['error']}")
            return None

    def is_user_in_channel(self, channel_id, user_id):
        try:
            response = self.client.conversations_members(channel=channel_id)
            if response["ok"]:
                return user_id in response["members"]
            else:
                print(f"Error fetching channel members: {response['error']}")
                return False
        except SlackApiError as e:
            print(f"Slack API Error: {e.response['error']}")
            return False

    def find_user_channels(self, user_id):
        # user_id = self.get_user_id(username)
        if user_id:
            channels = []
            channels = self.get_channels()
            user_channels = []

            for channel in channels:
                if self.is_user_in_channel(channel["id"], user_id):
                    user_channels.append(channel["name"])
                    print(channel["name"])

            return user_channels
        else:
            return []
        

    def all_channels(self):
        channels = []
        seen_channel_ids = set()
        cursor = None

        try:
            while True:
                if cursor:
                    response = self.client.conversations_list(types="public_channel,private_channel", cursor=cursor)
                else:
                    response = self.client.conversations_list(types="public_channel,private_channel")

                if response["ok"]:
                    for channel in response["channels"]:
                        if channel["id"] not in seen_channel_ids:
                            channels.append({"id": channel["id"], "name": channel["name"]})
                            seen_channel_ids.add(channel["id"])

                    cursor = response.get("response_metadata", {}).get("next_cursor")

                    # Break the loop if there are no more pages
                    if not cursor:
                        break
                else:
                    print(f"Error fetching channels: {response['error']}")
                    break
        except SlackApiError as e:
            print(f"Slack API Error: {e.response['error']}")

        # Save channels to a CSV file
        csv_file = 'channels.csv'
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["id", "name"])
            writer.writeheader()
            for channel in channels:
                writer.writerow(channel)
        # print("**************************")
        # print(response)
        return channels
            
#Default Test
if __name__ == "__main__":

    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    

    user_token = os.getenv('USER_TOKEN')
    manager = SlackChannelManager(token=user_token)
    
    # user_id = 'U074B0YNB7F' #Note Taken from the profile not from channel
    # channel_name = 'C0757KFK6Q0'

    # manager.remove_user_from_channel(user_id, channel_name)
    # manager.add_user_to_channel(user_id, channel_name)
    # manager.find_user_channels('dummy_acc')
