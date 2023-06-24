from abc import ABC

from deepstroy_model_service.base.processing_model_base import ProcessingModelBase


class ForecastingModel(ProcessingModelBase, ABC):
    def __init__(self):
        super().__init__()

    def process_data(self, bytes_data):
       pass
