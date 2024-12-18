
from datetime import datetime

from dependency_injector.wiring import inject, Provide

from src.Containers.AIModelContainer import AIModelContainer
from src.Entities.Dtos import  threadDto, userMessageInputDto, \
    MessageDto, actionDto
from src.Models import AIModel


class AIController:
    @inject
    def __init__(self, ai_model: AIModel = Provide[AIModelContainer.ai_model]):
        self.ai_model = ai_model
    async def get_history(self, userid: str) -> list[MessageDto]:
        result = self.ai_model.get_history_by_userid(userid)
        return result

    async def send_message(self, msg: userMessageInputDto) -> MessageDto:
        #session expired ?
        #create a new thread if thread_id is 0 or session expired
        if msg.thread_id == 0:
            msg.thread_id = self.ai_model.create_new_thread(threadDto(user_id = msg.user_id, device_id = msg.device_id))
        elif self.ai_model.is_thread_expired(msg.thread_id):
            msg.thread_id = self.ai_model.create_new_thread(threadDto(user_id = msg.user_id, device_id = msg.device_id))
        if msg.thread_id == -1:
            return None
        #inserting user msg to db
        result = self.ai_model.add_user_msg(msg)



        # processing and mapping
        # retrieve params thread and state

        # generate system msg

        # inserting system msg to db
        action=None
        action = actionDto(name="account_statement", params={"civil_id":"545454544554"})
        response = MessageDto(thread_id=msg.thread_id, content=  "Can I help you?",action=action, is_system=True, sent_at=datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f'))
        result = self.ai_model.add_system_msg(response)
        return response