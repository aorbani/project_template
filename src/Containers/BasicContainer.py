from dependency_injector import containers, providers
from  src.Models.dbConnection import DBConnection

class BasicContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.Models.AIModel"])
    config = providers.Configuration()
    db_connection=providers.Singleton(
        DBConnection
    )