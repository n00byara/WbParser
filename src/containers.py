from dependency_injector import containers, providers

from bot import create_bot, create_dispatcher
from core import Config
from parser import Parser
from parser import ParserService

class Container(containers.DeclarativeContainer):
    config: Config = providers.Singleton(Config)

    bot = providers.Singleton(
        create_bot,
        token=providers.Callable(lambda cfg: cfg.token, config)
    )
    dispatcher = providers.Singleton(create_dispatcher)

    parser_service: ParserService = providers.Singleton(ParserService)

    parser = providers.Singleton(Parser, parser_service=parser_service)

async def init_services(container: Container):
    service = container.parser_service()
    await service.start()
    return service