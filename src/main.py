import asyncio

from bot import setup_routers
from bot.handlers import handlers
from containers import Container

async def main():
    container = Container()
    container.init_resources()
    container.wire(modules=[handlers])

    bot = container.bot()
    dp = container.dispatcher()
    setup_routers(dp)
    parser_service = container.parser_service()

    await asyncio.gather(
        parser_service.start(),
        dp.start_polling(bot)
    )

if __name__ == "__main__":
    asyncio.run(main())