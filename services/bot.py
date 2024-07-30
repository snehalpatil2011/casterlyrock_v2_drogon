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
    refreshToken.start()

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")

@bot.command()
async def restart(ctx):
    if send_message.is_running() == True :
        send_message.stop()
        send_message.start()
    else:
        send_message.start()

    if refreshToken.is_running() == True :
        refreshToken.stop()
        refreshToken.start()
    else:
        refreshToken.start()
    await ctx.send("Restart Completed")

@bot.command()
async def stop(ctx):
    if send_message.is_running() == True :
        send_message.stop()

    if refreshToken.is_running() == True :
        refreshToken.stop()
    await ctx.send("Stop Completed")

@bot.command()
async def start(ctx):
    if send_message.is_running() == True :
        send_message.stop()
        send_message.start()
    else:
        send_message.start()

    if refreshToken.is_running() == True :
        refreshToken.stop()
        refreshToken.start()
    else:
        refreshToken.start()
    await ctx.send("Start Completed")

@bot.command()
async def gettoken(ctx):
    bt = BotUtils()
    await bt.refreshToken()
    await ctx.send("Refresh Token Completed")

@bot.command()
async def getposition(ctx):
    botutils = BotUtils()
    positionsData = await botutils.getPositions()
    await ctx.send(embed=positionsData)

@bot.command()
async def kill(ctx):
    botutils = BotUtils()
    res = await botutils.kill()
    await ctx.send(res)

async def sendMessageToChannel(message:str):
    channel = bot.get_channel(1267471110606290958)
    if channel:
        await channel.send(message)
        return {"status": "Message sent To Discord"}
    else:
        return {"status": "Channel not found"}
    
@tasks.loop(seconds=30)
async def send_message():
    channel = bot.get_channel(1267471110606290958)
    if channel:
        botutils = BotUtils()
        positionsData = await botutils.getPositions()
        await channel.send(embed=positionsData)

@send_message.before_loop
async def before_send_message():
    await bot.wait_until_ready()

#TOKEN is VAlid for 1 hour
@tasks.loop(minutes=40)
async def refreshToken():
    bt = BotUtils()
    await bt.refreshToken()
 
@refreshToken.before_loop
async def before_refreshToken():
    await bot.wait_until_ready()


# Add other bot commands and events here