import asyncio

from functools import wraps

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

class ParserService:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    # Запускаем браузер и создаем пустую страницу
    async def start(self) -> dict:
        self.playwright = await async_playwright().__aenter__()
        self.browser = await self.playwright.chromium.launch(headless=True, slow_mo=50)
        self.context = await self.browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
                viewport={"width": 1920, "height": 1080},
                screen={"width": 1920, "height": 1080},
                locale="ru-RU",
                device_scale_factor=1,
                is_mobile=False,
                has_touch=False,
                java_script_enabled=True
        )
        self.page = await self.context.new_page()

    async def close(self):
        await self.context.close()
        await self.browser.close()
        await self.playwright.stop()

    # Декоратор для получешиня страницы товара
    @staticmethod
    def get_page(func):
        @wraps(func)
        async def wrapper(this, *args, **kwargs):
            url = args[0] if args else ''

            if len(args) == 2:
                find_class = args[1] if args else None

            if url is None:
                raise ValueError('URL должен быть передан как аргумент')

            page = getattr(this, 'page', None) or getattr(getattr(this, 'service', None), 'page', None)

            if page is None:
                raise AttributeError("Page не найден в объекте или в service")

            script = """
    // Отключаем navigator.webdriver
    Object.defineProperty(navigator, 'webdriver', {
        get: () => false,
    });

    // Патчим window.chrome, чтобы не выглядел пустым
    window.chrome = {
        runtime: {},
        // можно добавить другие свойства при необходимости
    };

    // Переопределяем navigator.permissions.query для корректного ответа
    const originalQuery = window.navigator.permissions.query;
    window.navigator.permissions.query = (parameters) => {
        if (parameters.name === 'notifications') {
            return Promise.resolve({ state: Notification.permission });
        }
        return originalQuery(parameters);
    };

    // Переопределяем navigator.plugins — должен быть непустым массивом
    Object.defineProperty(navigator, 'plugins', {
        get: () => [1, 2, 3, 4, 5],
    });

    // Переопределяем navigator.languages для имитации настоящих настроек
    Object.defineProperty(navigator, 'languages', {
        get: () => ['ru-RU', 'ru'],
    });
"""
            try:
                await page.add_init_script(script)
                await page.goto(url, wait_until='domcontentloaded')

                await page.mouse.wheel(0, 1000)
                await page.keyboard.press('PageDown')

                # if find_class != '':


                await page.wait_for_selector(find_class, timeout=4000)
            except PlaywrightTimeoutError:
                print(f"[WARN] Timeout: элемент {find_class} не найден по адресу {url}")

            return await func(this, *args, **kwargs)

        return wrapper