
from pydantic import BaseModel
from typing import Generic, TypeVar
#example

class complaintDto(BaseModel):
    content: str
class ComplaintClassificationDto(BaseModel):
    content:   str
    channel:str
    class_name:  str

class ClassesDto(BaseModel):
    class_key:str
    class_name: str
T = TypeVar('T')

class ResponseDto(BaseModel ,Generic[T]):
    status: bool
    data: list[T]|T|str

