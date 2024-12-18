
import logging
from fastapi import APIRouter,  status, Response

from src.Entities.Dtos import complaintDto
from src.Containers.ControllerContainer import ControllerContainer as Container
from src.Entities.Dtos import ResponseDto


class router:
    def __init__(self):
        self.api_controller = Container.controller()
        self.router = APIRouter(responses={404: {"description": "Not found"}})
        self.router.add_api_route("/complaints/classify", self.classify, methods=["POST"], tags=['Complaints Classification'])

    async def classify(self,response: Response, comp: complaintDto)-> ResponseDto[str]:
        try:
            class_name = await self.api_controller.classify(comp)
            return ResponseDto(status=True,data=class_name)
        except Exception as e:
            logging.error(msg=str(e))
            response.status_code = status.HTTP_404_NOT_FOUND
            return ResponseDto(status=False,data=f"Something went wrong. Please try again later.")