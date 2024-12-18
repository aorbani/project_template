import logging
import sqlalchemy
import os

import oracledb
from src.Models.Helper import reformat_pwd

internal_env_vars = False
def isOpen(connectionObject):
    try:
        return connectionObject.ping() is None
    except Exception as ex:
        return False
class DBConnection:
    __sqlAIEngine = None
    def getSQLAIEngine(self):
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
    def getOraclecursor(self):
        try:
            if isOpen(self.__oracleConnection):
                return self.__oracleCursor
            connection_string_var = 'db_orc_kfhonline_connectionstring' +('_internal' if internal_env_vars is True else '')
            oracledb.init_oracle_client(lib_dir=r"C:\oracle\instantclient_21_13")
            self.__oracleConnection = oracledb.connect(connection_string_var)

            if self.__oracleConnection:
                self.__oracleCursor = self.__oracleConnection.cursor()
                logging.info("Connected to KfhOnline Oracle DB successfully")
                return self.__oracleCursor
            else :
                logging.info("Unable to Connect")
        except Exception as e:
            logging.error(msg=str(e) + self.__class__.__name__)
            logging.info("Something went wrong. Unable to connect to KfhOnline Oracle DB")

