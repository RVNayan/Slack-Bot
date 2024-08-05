# Slack Bot

![Slack API](https://a.slack-edge.com/80588/img/services/api_200.png)

## What Does It Do?

This Slack bot integrates seamlessly with Slack and offers the following exclusive features:

- **Retrieve the names of all channels** for a specific user within your organization.
- **Bulk add or remove users** from any channel efficiently.

## Commands

Here are the available commands for interacting with the bot:

- **`add @user_name #channel_name`**: Adds a user to a specified channel.
- **`remove @user_name #channel_name`**: Removes a user from a specified channel.
- **`get_channels @user_name`**: Retrieves the list of channels a user is part of.

## Prerequisites

Before setting up the Slack bot, ensure you have met the following requirements:

1. **Create a Slack App**:
   - Visit the [Slack API website](https://api.slack.com/apps) to create your app.

2. **Assign Permissions**:
   - Ensure the bot has the necessary permissions for the tasks it will perform.

3. **Generate and Store Tokens**:
   - Copy the following keys and create a `.env` file:
     - `USER_TOKEN`
     - `BOT_TOKEN`
     - `SIGNING_SECRET`
     - `SLACK_API_TOKEN`
     - `SLACK_CLIENT_ID`
     - `SLACK_CLIENT_SECRET`
     - `FLASK_SECRET_KEY` (Generate from Terminal)

4. **Install Required Libraries**:
   - Install all necessary libraries as listed [here](requirements.txt).

5. **Set Up HTTP Tunnel**:
   - Create an HTTP tunnel using [ngrok](https://ngrok.com/) and configure it in your Event Subscription settings. Ensure necessary Bot events are subscribed to.

6. **Add the App to Your Channel**:
   - Ensure the app is added to your Slack channel before running the code.

## Installation

To install and set up the Slack bot, follow these steps:

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/slack-bot.git
   cd slack-bot
