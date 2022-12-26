from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject

from .translate_word import TranslateWordService


class ParserContainer(containers.DeclarativeContainer):
    
    # config = providers.Resource(DevSettings)
    
    translate_service = providers.Factory(
        TranslateWordService
    )
