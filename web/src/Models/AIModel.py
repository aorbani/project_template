import json
import logging
from datetime import datetime, timedelta

import pandas as pd
from dependency_injector.wiring import inject, Provide
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.Entities.Dtos import threadDto, MessageDto, userMessageInputDto
from src.Entities.Entities import Thread, Message
from src.Entities.mapper import map_message_history_dto, model_to_dict, map_user_message_to_entity, \
    map_system_message_to_entity, map_thread_to_entity
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
            self.__sqlengine = self.__con.getAIEngine()


    def get_history_by_userid(self, user :str) -> list[MessageDto]:
        self.init_sql_engine()

        with Session(self.__sqlengine) as session:

            try:
                history = session.query(Message).join(Thread, Thread.thread_id == Message.thread_id).where(Thread.user_id == user).where(Thread.active == True).all()

            except Exception as e:
                logging.error(f"An error occured: {e}")
                session.rollback()
            finally:
                session.close()

        if history is not None:
            history_df = pd.DataFrame([model_to_dict(item) for item in history])
            return map_message_history_dto(history_df)
        return []

    def create_new_thread(self, thread :threadDto) -> int|None:
        if self.has_active_thread(thread.user_id):
            return -1
        self.init_sql_engine()
        thread_entity= map_thread_to_entity(thread)

        with Session(self.__sqlengine) as session:
            try:
                session.add(thread_entity)
                session.commit()
                return thread_entity.thread_id
            except Exception as e:
                logging.error(f"An error occured: {e}")
                session.rollback()
            finally:
                session.close()
        return 0
    def has_active_thread(self, user_id)-> bool:
        self.init_sql_engine()

        with Session(self.__sqlengine) as session:
            try:
                thread_id = session.query(Thread.thread_id).where(Thread.active == True).where(Thread.user_id == user_id).one_or_none()
                return thread_id is not None
            except Exception as e:
                logging.error(f"An error occured: {e}")
                session.rollback()
            finally:
                session.close()
        return None
    def add_system_msg(self, msg :MessageDto) -> bool:
        self.init_sql_engine()
        msg_entity= map_system_message_to_entity(msg)

        with Session(self.__sqlengine) as session:
            try:
                session.add(msg_entity)
                session.commit()
                return True
            except Exception as e:
                logging.error(f"An error occured: {e}")
                session.rollback()
            finally:
                session.close()
        return False
    def update_system_msg(self, thread_id :int,action:str,params:str) -> bool:
        self.init_sql_engine()

        with Session(self.__sqlengine) as session:
            try:
                last_msg_id = session.query(Message.msg_id).where(Message.thread_id == thread_id).order_by(Message.sent_at.desc()).one_or_none()
                session.execute(update(Message).where(Message.msg_id == last_msg_id)
                                .values(action=action, params=params))
                session.execute(update(Thread).where(Thread.thread_id == thread_id)
                                .values(action=action, params=params))
                session.commit()
                return True
            except Exception as e:
                logging.error(f"An error occured: {e}")
                session.rollback()
            finally:
                session.close()
        return False

    def add_user_msg(self, msg :userMessageInputDto) -> bool:
        self.init_sql_engine()
        msg_entity=map_user_message_to_entity(msg)
        with Session(self.__sqlengine) as session:
            try:
                session.add(msg_entity)
                session.commit()
                return True
            except Exception as e:
                logging.error(f"An error occured: {e}")
                session.rollback()
            finally:
                session.close()
        return False

    def get_thread_params(self, thread_id :int) -> None:
        self.init_sql_engine()

        with Session(self.__sqlengine) as session:
            try:
                params = session.query(Thread.params).where(Thread.thread_id == thread_id).one_or_none()
                return json.loads(params)
            except Exception as e:
                logging.error(f"An error occured: {e}")
                session.rollback()
            finally:
                session.close()
        return None
    def is_thread_expired(self, thread_id :int) -> bool:
        self.init_sql_engine()

        with Session(self.__sqlengine) as session:
            try:
                last_activity = session.query(Thread.last_activity).where(Thread.thread_id == thread_id).one_or_none()
                expired = (datetime.today() - timedelta(minutes=15)) > datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S.%f')
                if expired:
                    session.execute(update(Thread).where(Thread.thread_id == thread_id)
                                    .values(active=False, expired_at=datetime.today()))
                    session.commit()
                return expired
            except Exception as e:
                logging.error(f"An error occured: {e}")
                session.rollback()
            finally:
                session.close()
