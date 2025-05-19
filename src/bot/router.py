from aiogram import Dispatcher
from bot.handlers.commands import router as commands_router
from bot.handlers.handlers import router as handlers_router


def setup_routers(dp: Dispatcher):
    dp.include_router(commands_router)
    dp.include_router(handlers_router)