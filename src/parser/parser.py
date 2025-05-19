from typing import List
import re

from playwright.async_api import ElementHandle, Page

from parser import ParserService
from parser.items import Item

class Parser:
    title = None
    def __init__(self, parser_service: ParserService) -> None:
        self.service = parser_service

    # Поиск просто по названию
    # Можно произвести более детальный по product-params(характеристики товара)
    @ParserService.get_page
    async def __get_title(self, url: str, find_class: str) -> str:
        title: ElementHandle = await self.service.page.query_selector('.product-page__title')
        return await self.service.page.content()

    @ParserService.get_page
    async def __get_item_info(self, url: str, find_class: str) -> Item:
        title_html: ElementHandle = await self.service.page.query_selector('.product-page__title')
        price_html: ElementHandle = await self.service.page.query_selector('.price-block__wallet-price')
        image_html: ElementHandle = await self.service.page.query_selector('.photo-zoom__preview.j-zoom-image.hide')
        src = await image_html.get_attribute('src')

        try:

            title = await title_html.text_content()
            # src = await src_html.text_content()
            price = await price_html.text_content()
            # Заменяем пробелы(если цена больше 1000) и удаляем символ ₽
            price = re.sub(r"[^\d]", "", price)
            return Item(
                title=title,
                price=int(price),
                url=url,
                image_url=src,
            )
        except Exception:
            return None

    @ParserService.get_page
    async def __get_a_handles(self, url: str, find_class: str):
        content = await self.service.page.content()
        items: ElementHandle = await self.service.page.query_selector_all('product-card j-card-item j-analitics-item  ')

        return await self.service.page.query_selector_all('.product-card__wrapper')

    async def __get_hrefs_from_handles(self, a_handles):
        hrefs = []
        for a_handle in a_handles:
            a = await a_handle.query_selector("a")
            href = await a.get_attribute("href")
            if href:
                hrefs.append(href)

        return hrefs

    async def get_items_list(self, url: str) -> List[Item]:
        find_item = await self.__get_item_info(url, '.product-page__header')

        a_handles = await self.__get_a_handles(f"https://www.wildberries.ru/catalog/0/search.aspx?search={find_item.title}", '.catalog-page')

        hrefs = await self.__get_hrefs_from_handles(a_handles)

        elements = []

        for href in hrefs:
            element = await self.__get_item_info(href, '.product-page__header')
            if element:
                elements.append(element)

        return elements