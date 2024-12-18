import logging

from dependency_injector.wiring import Provide, inject

from src.Containers.AIModelContainer import AIModelContainer
from src.Entities.Dtos import complaintDto
from src.Models import AIModel


class Controller:
    classes = None
    @inject
    def __init__(self, ai_model: AIModel = Provide[AIModelContainer.ai_model]):
        self.ai_model = ai_model
        self.init_class()

    def init_class(self):
        self.classes = self.ai_model.get_complaint_classes()
    async def classify(self, comp: complaintDto) -> str:
        class_name = self.classifier.classify(comp.content)
        added = self.ai_model.add_complaint_classification(comp,class_name)
        if added:
            logging.info("complaint classified and logged successfully")
        else:
            logging.error("Unable to log complaint's classification")
        return class_name