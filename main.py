from telegram_parser import TelegramParser
from telegram_analyzer import TelegramAnalyzer
from visualizer import Visualizer
from transformers import logging
import asyncio
import warnings
warnings.filterwarnings('ignore')
logging.set_verbosity_error()
warnings.filterwarnings("ignore", message="You seem to be using the pipelines sequentially on GPU")

# ======= SETTINGS ======
API_ID = 35422623
API_HASH = '48339feda0da402762395e3e1f0c349b'
PHONE = '89932746331'

CHANNEL = "artemmetelev"
POSTS_LIMIT = 1000
# ==============================


async def main():
    # 1. Parsing channel
    parser = TelegramParser(api_id=API_ID, api_hash=API_HASH, phone=PHONE)
    await parser.connect()
    json_path = await parser.parse_and_save(channel=CHANNEL, limit=POSTS_LIMIT)
    await parser.disconnect()

    # 2. Analysing data
    analyzer = TelegramAnalyzer(json_file=str(json_path))
    dataframe = analyzer.analyze()
    analyzer.print_stats()

    # 3. Visualize data
    #visualizer = Visualizer(source=dataframe)
    #visualizer.create_dashboard()

if __name__ == '__main__':
    asyncio.run(main())


