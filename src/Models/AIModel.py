import json
import logging
from datetime import datetime, timedelta
from typing import Tuple, Any, Optional

import numpy as np
import pandas as pd
from dependency_injector.wiring import inject, Provide
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.Entities.Entities import Classes
from src.Entities.mapper import  modellist_to_dict
from src.Models.dbConnection import DBConnection
from src.Containers.BasicContainer import BasicContainer as Container


class model:
    __sqlengine = None
    @inject
    def __init__(self,con: DBConnection = Provide[Container.db_connection]):
        self.__con = con
        self.customer_habits= None
    def init_sql_engine(self):
        if self.__sqlengine is None:
            self.__sqlengine = self.__con.getSQLAIEngine()
# the below are examples only and needs to be removed


    '''def is_thread_expired(self, thread_id :int) -> bool:
        self.init_sql_engine()

        with Session(self.__sqlengine) as session:
            try:
                active = session.query(Thread.active).where(Thread.thread_id == thread_id).one_or_none()
                return not active[0]
            except Exception as e:
                logging.error(f"An error occured: {e}")
                session.rollback()
            finally:
                session.close()
    def add_complaint_classification(self,comp,class_name):
        self.init_sql_engine()
        comp = map_complaint_to_entity(comp,class_name)
        with Session(self.__sqlengine) as session:
            try:
                session.add(comp)
                session.commit()
                return True
            except Exception as e:
                logging.error(f"An error occured: {e}")
                session.rollback()
            finally:
                session.close()
        return False'''

    def get_complaint_classes(self):
        self.init_sql_engine()
        with Session(self.__sqlengine) as session:
            try:
                classes = session.query(Classes).all()
                return modellist_to_dict(classes)
            except Exception as e:
                logging.error(f"An error occured: {e}")
                session.rollback()
            finally:
                session.close()
        return None

