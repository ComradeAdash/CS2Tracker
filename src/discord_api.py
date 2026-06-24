import steam_skins
import discord
import weapon_skin
from discord.ext import commands
from discord import app_commands

GUILD_ID = discord.Object(id=1277759001123360800)
GUILD_ID_2 = discord.Object(id=1505726620424474624)

class Client(commands.Bot):
    async def on_ready(self):                      # when the bot has connected to the server
        print(f'We have logged in as {self.user}')

        try:
            guild = discord.Object(id=GUILD_ID_2.id)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guld {guild.id}.')
        except Exception as e:
            print(f'Error syncing commands: {e}')

    async def on_message(self, message):           #  when a message is sent in the server
        if message.author == self.user:
            return                                 # the bot shouldn't respond to itself
        
        if message.content.startswith('meow'):
            await message.channel.send(f'MEOW') 

intents = discord.Intents.default()                # this is required to specify what the bot can do
intents.message_content = True
client = Client(command_prefix='!', intents=intents)

@client.tree.command(name="hello",description="Says hello to the user", guild=GUILD_ID_2)
async def sayHello(interaction: discord.Interaction):
    await interaction.response.send_message("Hi There!")

# /skin "slash" command
@client.tree.command(name="skin",description="Displays the lowest price and median price of a selected weapon", guild=GUILD_ID_2)
async def skin(interaction: discord.Interaction, skin: str): # the skin is the user input over here
    await interaction.response.defer()

    result = weapon_skin.search_skin(skin)
    embed = discord.Embed(title=" ", description=" ")
    # await interaction.response.send_message(embed=embed) NOT SURE IF THIS IS NEEDED
    
    if result:
        skin_name = result
        data = steam_skins.fetch_request(skin_name, steam_skins.parameters)
        print(data)

        # format the information in our embed over here

        embed.add_field(name="Results!!", value=f''' Skin Lemur has found {skin_name}!! OHHHhh YEAHHhh!! ''')
        embed.add_field(name="Lowest Price: ", value = f''' {data.get('lowest_price')} ''')
        embed.add_field(name="Median Price: ", value = f''' {data.get('median_price')} ''')


        await interaction.followup.send(embed=embed)
    else:
        await interaction.followup.send("Skin not found or invalid query.")

    