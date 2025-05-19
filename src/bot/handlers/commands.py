from aiogram import types, Router
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Бот запущен.\nДля получения списка товаров введите ссылку на товар. Пример: https://www.wildberries.ru/catalog/256525133/detail.aspx\nКоличество подобраных товаров будет ограничено 30\nЗагрузка товаров занимает определенное время, после отправки ссылки придется немного подождать")
