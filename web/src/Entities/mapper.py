import json

import pandas as pd

from src.Entities.Dtos import MessageDto, threadDto, actionDto, userMessageInputDto
from src.Entities.Entities import Message, Thread


def model_to_dict(instance): #this method converts the entities to dict, to transform to datafarme later on.
    return {key: value for key, value in instance.__dict__.items() if not key.startswith('_')}
def map_message_history_dto(input: pd.DataFrame)-> list[MessageDto]:
    dtos = []

    for _,row in input.iterrows():
        action = None
        if row['action'] is not None:
            action = actionDto(name=row['action'],params=json.loads(row['params']))
        dto = MessageDto(
                thread_id= row['thread_id'],
                content= row['msg_content'],
                is_system= row['sender'] == 'system',
                action= action,
                sent_at= row['sent_at'])
        dtos.append(dto)
    return dtos


def map_user_message_to_entity(msg:userMessageInputDto)-> Message:
    return Message(thread_id=msg.thread_id,msg_content=msg.content,sender='user')

def map_thread_to_entity(thread:threadDto) -> Thread:
    return Thread(user_id=thread.user_id,device_id=thread.device_id, channel=thread.channel, active= thread.active)


def map_system_message_to_entity(msg:MessageDto)-> Message:
    return Message(thread_id=msg.thread_id,msg_content=msg.content,sender='system',action=msg.action.name,params=json.dumps(msg.action.params))