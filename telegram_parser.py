from telethon import TelegramClient
from tqdm import tqdm
from base_parser import BaseParser
from typing import Dict, List


class TelegramParser(BaseParser):
    def __init__(self, api_id: int, api_hash: str, phone: str, session_name: str = "session"):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone = phone
        self.client = None
        self.session_name = session_name

    async def connect(self):
        print("Connecting to Telegram...")
        self.client = TelegramClient(self.session_name, self.api_id, self.api_hash)
        await self.client.start(phone=self.phone)
        print(f"Connected")

    async def disconnect(self):
        if self.client:
            await self.client.disconnect()
            print("Disconnected")

    async def parse(self, channel: str, limit: int = 100, text_len: int = 2000, **kwargs) -> List[Dict]:
        if not self.client:
            raise RuntimeError("Client not connected")
        print(f"Starting parse: channel - @{channel}, posts limit - {limit}")
        posts = []
        with tqdm(total=limit, desc="Collecting posts", unit="post") as pbar:
            async for msg in self.client.iter_messages(channel, limit=limit):
                if msg.text:
                    posts.append({
                        'text': msg.text[:text_len],
                        'date': str(msg.date),
                        'views': msg.views,
                        'forwards': msg.forwards,
                        'replies': msg.replies.replies if msg.replies else 0
                    })
                pbar.update(1)
        return posts
