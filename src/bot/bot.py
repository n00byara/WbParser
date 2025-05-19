from aiogram import Bot, Dispatcher

def create_bot(token: str) -> Bot:
    return Bot(token=token)

def create_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    return dp