import asyncio
import logging

from bot_config import bot, dp
from setup import register_routers
from setup import register_commands

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", force=True)
logger = logging.getLogger(__name__)

async def main():
    register_routers()
    await register_commands()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
