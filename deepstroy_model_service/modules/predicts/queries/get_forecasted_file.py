from deepstroy_model_service.domain import ForecastedFile
from deepstroy_model_service.domain.data_access_layer.session import session


class GetForecastedFileQuery:
    def __init__(self):
        pass

    def by_id(self, file_id: int) -> ForecastedFile:
        current_session = session()

        try:
            return current_session\
                .query(ForecastedFile)\
                .filter(ForecastedFile.id == file_id)\
                .one_or_none()

        finally:
            current_session.close()

        return