from dependency_injector import containers, providers
from src.Containers.BasicContainer import BasicContainer
from src.Models.AIModel import model as _AIModel

class AIModelContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.Controllers.Controller"])
    config = providers.Configuration()

    ai_model = providers.Singleton(
        _AIModel,
        con=BasicContainer.db_connection
    )

