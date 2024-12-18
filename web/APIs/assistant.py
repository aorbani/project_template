import json
import logging
from datetime import datetime

import response
from fastapi import APIRouter,  status, Header,Response
from src.Containers.ControllerContainer import ControllerContainer as Container
from src.Entities.Dtos import ResponseDto, userMessageInputDto


class assistant:
    def __init__(self):
        self.api_controller = Container.api_controller()
        self.router = APIRouter(responses={404: {"description": "Not found"}})
        self.router.add_api_route("/Assistant/get_history", self.get_history, methods=["GET"], tags=['Aurora Assistant'])
        self.router.add_api_route("/Assistant/send_message", self.send_message, methods=["POST"], tags=['Aurora Assistant'])
    async def get_history(self,response: Response, X_user_id: str= Header(None)) -> ResponseDto:
        try:
            history = await self.api_controller.get_history(X_user_id)
            return ResponseDto(status=True,data=history)
        except Exception as e:
            logging.error(msg=str(e))
            response.status_code = status.HTTP_404_NOT_FOUND
            return ResponseDto(status=False,data=f"Something went wrong. Please try again later.")

    async def send_message(self,response: Response, msg: userMessageInputDto)-> ResponseDto:
        try:
            system_msg = await self.api_controller.send_message(msg)
            return ResponseDto(status=True,data=system_msg)
        except Exception as e:
            logging.error(msg=str(e))
            response.status_code = status.HTTP_404_NOT_FOUND
            return ResponseDto(status=False,data=f"Something went wrong. Please try again later.")