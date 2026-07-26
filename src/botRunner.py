'''

Discord Bot Runner

'''

import bot.discord_api as discord_api
import config as cfg

if __name__ == "__main__":
    print("Running the bot :p ...")
    discord_api.client.run(cfg.DISCORD_TOKEN)