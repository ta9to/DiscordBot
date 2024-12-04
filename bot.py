import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openAIClient = OpenAI(
    api_key=OPENAI_API_KEY,
)

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

@bot.command(name='tft')
async def opgg(ctx, username: str):
    tftopgg_url = f"https://tft.op.gg/summoners/jp/{username}-JP1"
    await ctx.send(f"{username}のTFT.OP.GG URLは: {tftopgg_url}")

message_history = {}
system_prompt = """
あなたは「金子豚」という名前のAIアシスタントです。
あなたはDiscordサーバーで動作し、ユーザーがLeague of Legends（LoL）について質問をした際に助けを提供します。
LoLのチャンピオン、ゲームのメカニクス、戦略、そしてカウンターピックについての深い知識を持っています。

以下はあなたの行動指針です：
1. 友好的で親切な口調で話してください。ユーザーがあなたを友達だと感じられるようにしましょう。
2. 専門的な回答を提供します。例えば、カウンターピックが質問された場合、具体的なチャンピオンの名前と、そのチャンピオンを使った立ち回り方を詳しく説明します。
   - 例: 「カウンターピックの質問に対しては、このように答えます。『例えば、相手がYasuoなら、Malzaharを使うと良いですよブー。MalzaharのアルティメットはYasuoの風の壁を無効化できて、相手をコントロールできるからブー。また、レーン戦では、Yasuoが近づいてきたときにEスキルでシールドを外すと有利に立ち回れますブー。』とねブー。」
3. 嘘をつかないでください

この設定を守り、LoLについての質問に答えてください。
"""

@bot.event
async def on_message(message):
    # メンションされたかどうかを確認
    if bot.user.mentioned_in(message):
        # 自己メンションの場合（bot同士のメンション）を除外
        if message.author == bot.user:
            return

        # チャンネルIDをキーに履歴を管理
        channel_id = message.channel.id
        if channel_id not in message_history:
            message_history[channel_id] = []

        # 現在のメッセージを履歴に追加
        content = message.content.replace(f'<@{bot.user.id}>', '').strip()
        message_history[channel_id].append({"role": "user", "content": content})
        message_history[channel_id] = message_history[channel_id][-20:]

        try:
            print(f"Channel {channel_id} history:\n{message_history[channel_id]}")
            response = openAIClient.chat.completions.create(
                model="gpt-4o-mini",
                messages = [{"role": "system", "content": system_prompt}] + message_history[channel_id]
            )
            response_message = response.choices[0].message.content
            await message.channel.send(response_message)
            message_history[channel_id].append({"role": "assistant", "content": response_message})
        except Exception as e:
            await message.channel.send(f"エラーが発生しました: {str(e)}")

    await bot.process_commands(message)

bot.run(TOKEN)
