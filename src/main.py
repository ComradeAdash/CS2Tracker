# This is how the whole program will be ran at the end

import bot.discord_api as discord_api
from dotenv import load_dotenv
import os

load_dotenv(".env")
token = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
    print("Running the bot :p ...")
    discord_api.client.run(token)