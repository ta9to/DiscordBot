import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from openai import OpenAI
from openai_handler import OpenAIHandler

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openAIClient = OpenAI(
    api_key=OPENAI_API_KEY,
)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
open_ai = OpenAIHandler()

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

@bot.command(name='tft')
async def opgg(ctx, username: str):
    tftopgg_url = f"https://tft.op.gg/summoners/jp/{username}-JP1"
    await ctx.send(f"{username}のTFT.OP.GG URLは: {tftopgg_url}")

@bot.event
async def on_message(message):
    # メンションされたかどうかを確認
    if bot.user.mentioned_in(message):
        # 自己メンションの場合（bot同士のメンション）を除外
        if message.author == bot.user:
            return

        channel_id = message.channel.id
        content = message.content.replace(f'<@{bot.user.id}>', '').strip()
        open_ai.add_message(channel_id, "user", content)

        try:
            response_message = await open_ai.generate_response(channel_id)
            await message.channel.send(response_message)
        except Exception as e:
            await message.channel.send(f"エラーが発生しました: {str(e)}")

    await bot.process_commands(message)

bot.run(TOKEN)
