# Simplest Telegram Bot Demo
 A very minimal setup to create a Telegram bot hosted on Heroku.

## Local Setup

### Create a python virtual environment

Use your favourite virtual environment manager.

### Install packages

This command installs all the necessary packages into your current active environment:

`make install`

### Set up environment variables

Create `.env` file in the project root. It is already added to `.gitignore`. Add your telegram bot key to `.env`:
```
TELEGRAM_BOT_KEY=<your_bot_key>
```

###  Start the bot on your local machine

`python app.py`
