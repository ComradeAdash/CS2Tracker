'''

Configs for discord, database, .env

'''

import os
from dotenv import load_dotenv

# Ensure we load the .env file located in the same directory as this config file
_here = os.path.dirname(__file__)
load_dotenv(os.path.join(_here, ".env"))

DATABASE_URL = os.getenv("DATABASE_URL")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")