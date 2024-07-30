import discord
from discord.ext import commands,tasks
from services.botutils import BotUtils

intents = discord.Intents.default()
intents.message_content = True  # Ensure you have the message content intent

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    send_message.start()

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")

async def sendMessageToChannel(message:str):
    channel = bot.get_channel(1267471110606290958)
    if channel:
        await channel.send(message)
        return {"status": "Message sent To Discord"}
    else:
        return {"status": "Channel not found"}
    
@tasks.loop(minutes=1)
async def send_message():
    channel = bot.get_channel(1267471110606290958)
    if channel:
        botutils = BotUtils()
        positionsData = await botutils.getPositions()
        await channel.send(embed=positionsData)

@send_message.before_loop
async def before_send_message():
    await bot.wait_until_ready()

# Add other bot commands and events here