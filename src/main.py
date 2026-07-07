'''

Main Driver

'''

import bot.discord_api as discord_api
import config

if __name__ == "__main__":
    print("Running the bot :p ...")
    discord_api.client.run(config.DISCORD_TOKEN)