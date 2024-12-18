import json
from typing import List

import pandas as pd
from pandas import isnull

from src.Entities.Dtos import complaintDto
from src.Entities.Entities import ComplaintClassification


def model_to_dict(instance): #this method converts the entities to dict, to transform to datafarme later on.
    return {key: value for key, value in instance.__dict__.items() if not key.startswith('_')}
def modellist_to_dict(instances):
    classes = {}
    for instance in instances:
        dictkey = instance.class_name
        dictvalue = instance.class_key
        classes[dictkey] = dictvalue
    return classes
'''def map_message_history_dto(input: pd.DataFrame)-> list[APIMessageDTO]:
    dtos = []
    for _,row in input.iterrows():
        action = None
        if row['action'] is not None:
            action = actionDto(name=row['action'],params=json.loads(row['params']))
        dto = APIMessageDTO(
                thread_id= row['thread_id'],
                msg_id = row['msg_id'],
                sent_msg_id = None if isnull(row['sent_msg_id']) else int(row['sent_msg_id']),
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
    return Message(thread_id=msg.thread_id,msg_content=msg.content,sender='system',action=msg.action.name if msg.action is not None else None,
                   params=json.dumps(msg.action.params if msg.action and msg.action.params is not None else {}))
def map_complaint_to_entity(comp:complaintDto,class_name:str):
    return ComplaintClassification(content=comp.content,channel="RPA",class_name=class_name)

def map_msg_record_to_entity(msg: pd.DataFrame) -> MsgRecordDto:
    dto = None
    for _, row in msg.iterrows():
        action = None
        if row['action'] is not None:
            action = actionDto(name=row['action'], params=json.loads(row['params']))
        dto = MsgRecordDto(
            thread_id=row['thread_id'],
            msg_id=row['msg_id'],
            sender=row['sender'],
            msg_content=row['msg_content'],
            action=action,
            sent_at=row['sent_at'])
    return dto
'''