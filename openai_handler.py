from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class OpenAIHandler:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.system_prompt = """
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
        self.message_history = {}

    def add_message(self, channel_id, role, content):
        if channel_id not in self.message_history:
            self.message_history[channel_id] = []
        self.message_history[channel_id].append({"role": role, "content": content})
        # 過去20メッセージのみ保持
        self.message_history[channel_id] = self.message_history[channel_id][-20:]

    async def generate_response(self, channel_id):
        try:
            if channel_id not in self.message_history:
                return "まだメッセージ履歴がありません。"

            messages = [{"role": "system", "content": self.system_prompt}] + self.message_history[channel_id]
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            response_message = response.choices[0].message.content
            # 応答を履歴に追加
            self.add_message(channel_id, "assistant", response_message)
            return response_message
        except Exception as e:
            return f"エラーが発生しました: {str(e)}"