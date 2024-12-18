import os

import numpy as np
import pandas as pd
from datetime import timedelta, time
import logging
import re
from dependency_injector.wiring import Provide, inject
from src.Containers.BasicContainer import BasicContainer as Container
from src.Models.dbConnection import DBConnection

# get username from fraud trxs - TODO

internal_env_vars = False
class model:
    __oracle_cursor = None
    Master_data = None
    __batch_size = 500000
    @inject
    def __init__(self,
                 con: DBConnection = Provide[Container.db_connection]):
        self.__con = con
        self.schema = os.getenv('orc_schema' + ('_internal' if internal_env_vars is True else ''))
    def init_oracle_cursor(self):
        self.__oracle_cursor = self.__con.getOraclecursor()


    def get_customer(self, username:str):
        try:
            self.init_oracle_cursor()
            query = (f'select username, rim_no as rim from {self.schema}.CUSTOMER_PROFILES '
                     f'where  username = \'{username}\' and status != 5')

            self.__oracle_cursor.execute(query)

            data = self.__oracle_cursor.fetchone()
            if data is None:
                return data
            data_df = pd.DataFrame(data=[data],columns=['username', 'rim'])
            return data_df
        except Exception as e:
            logging.error(msg=str(e) + self.__class__.__name__)
            return None
    def get_recent_device_reg(self, end_date,username=None, Master_List = None):
        try:
            self.init_oracle_cursor()
            condition = f'd.CREATED_DATE > TO_DATE(\'{(end_date - timedelta(days=1)).strftime("%Y-%m-%d")}\',\'YYYY-MM-DD\')  \
            and d.CREATED_DATE < TO_DATE(\'{(end_date + timedelta(days=1)).strftime("%Y-%m-%d")}\',\'YYYY-MM-DD\')'
            if username is not None:
                condition+= f' and p.username =\'{username}\' '
            query=f'select p.username, count(d.device_id) from {self.schema}.customer_profiles p left join \
            {self.schema}.device_registration d on d.profile_id = p.profile_id where {condition} group by p.username'
            self.__oracle_cursor.execute(query)
            with open('logs/oracleQueries.txt', 'a') as f:
                f.write(query + '\n\n')
            data = self.__oracle_cursor.fetchall()
            data_df = pd.DataFrame.from_records(data, columns = ['username','recent_added_device'])
            data_df.recent_added_device=data_df.recent_added_device.astype('int32')
            data_df=data_df.set_index('username')
            data_df = data_df.sort_index()
            if Master_List is not None:
                return pd.concat([Master_List, data_df.reindex(Master_List.index, fill_value=0)], axis=1)
            return data_df
        except Exception as e:
            logging.error(msg=str(e) + self.__class__.__name__)
        return None

