from dependency_injector import containers, providers

from src.Containers.AIModelContainer import AIModelContainer
from src.Controllers.AIController import AIController


class ControllerContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["APIs.assistant"])
    config = providers.Configuration()

    api_controller = providers.Singleton(
        AIController,
        ai_model=AIModelContainer.ai_model)
