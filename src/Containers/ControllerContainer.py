from dependency_injector import containers, providers

from src.Controllers.Controller import Controller
from src.Containers.AIModelContainer import AIModelContainer


class ControllerContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(packages=["APIs.router"])
    config = providers.Configuration()


    controller = providers.Singleton(
        Controller,
        ai_model=AIModelContainer.ai_model)

