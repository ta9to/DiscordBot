import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_BOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot has logged in as {bot.user}')

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}!')

@bot.command(name='opgg')
async def opgg(ctx, username: str):
    opgg_url = f"https://www.op.gg/summoners/jp/{username}-JP1"
    await ctx.send(f"{username}のOP.GG URLは: {opgg_url}")

bot.run(TOKEN)
