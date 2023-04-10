from dependency_injector import containers, providers

from .translate_word import TranslateWordService


class ParserContainer(containers.DeclarativeContainer):
    
    # config = providers.Resource(DevSettings)
    
    translate_service = providers.Factory(
        TranslateWordService
    )
