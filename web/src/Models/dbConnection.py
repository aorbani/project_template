import logging
import sqlalchemy
import os

from src.Models.Helper import reformat_pwd

    
class DBConnection:
    __sqlAIEngine = None
    def getAIEngine(self):
        try:
            if self.__sqlAIEngine is not None:
                return self.__sqlAIEngine
            connection_string_var = 'db_sql_ai_connectionstring'
            self.__sqlAIEngine = sqlalchemy.create_engine(reformat_pwd(os.getenv(connection_string_var)),use_setinputsizes=False,echo=False)
            if self.__sqlAIEngine != None:
                logging.info("Connected to AI Sakher SQL DB ENGINE successfully")
                return self.__sqlAIEngine
            else:
                logging.info("Unable to Connect")
                return None
        except Exception as err:
            logging.error(msg=err)
            logging.info("Something went wrong. Unable to connect to AI Sakher SQL DB")

