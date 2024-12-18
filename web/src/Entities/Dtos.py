
from pydantic import BaseModel

class threadDto(BaseModel):
    user_id:  str
    device_id:str
    channel:str = "mobile app"
    active: bool = True


class userMessageInputDto(BaseModel):
    user_id:str
    device_id: str
    thread_id: int
    content:  str
class actionDto(BaseModel):
    name: str
    params: dict

class MessageDto(BaseModel):
    thread_id:int
    content:  str
    is_system:  bool
    action: actionDto|None
    sent_at : str

class ResponseDto(BaseModel ):
    status: bool
    data: list[MessageDto]|MessageDto|str

