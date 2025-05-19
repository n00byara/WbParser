import re
from typing import List

from aiogram import F, Router
from aiogram.types import Message
from dependency_injector.wiring import inject, Provide

from containers import Container
from parser.items import Item
from parser import Parser

router = Router()

URL_REGEX = re.compile(
    r'(?i)\b(?:https?://|www\.)\S+\.\S+'
)

def is_url(text: str) -> bool:
    return bool(URL_REGEX.search(text))

@router.message(F.text)
@inject
async def get_link_from_user(
        message: Message, parser: Parser = Provide[Container.parser],
):
    if is_url(message.text):
        items: List[Item] = await parser.get_items_list(message.text)

        for item in items:
            caption = f"Название товара: {item.title}\nЦена: {item.price}\nСсылка на товар: {item.url}"
            await message.answer_photo(photo=item.image_url, caption=caption)
    else:
        await message.answer(text="Введите ссылку!")