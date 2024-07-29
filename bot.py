import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True  # Ensure you have the message content intent

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send("Hello, world!")

# Add other bot commands and events here
