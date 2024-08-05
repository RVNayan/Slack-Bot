# Slack Bot

![Slack API](https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Slack_Technologies_Logo.svg/2560px-Slack_Technologies_Logo.svg.png)

## What Does it do?

This Slack app integration has the following exclusive features

→  Gets the names of all channels of a specific user of the organization
→ Bulk add/remove any number of users from any channel
## Commands

- **_add_ @user_name #channel_name**
- **_remove_ @user_name #channel_name**
- **_get_channels_ @user_name**


## Prerequisites

Before you begin, ensure you have met the following requirements:
1. Make sure you create a app in [Slack Website](https://api.slack.com/apps)
2. Assign the necessary permissions to the bot.
3. Copy the following keys and create a .env file
    USER_TOKEN, BOT_TOKEN, SIGNING_SECRET, SLACK_API_TOKEN, SLACK_CLIENT_ID, SLACK_CLIENT_SECRET, FLASK_SECRET_KEY (Generate from Terminal)
## Installation

To install and set up the Slack bot, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/slack-bot.git
   cd slack-bot
