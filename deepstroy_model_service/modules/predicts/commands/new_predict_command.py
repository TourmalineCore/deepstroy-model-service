from deepstroy_model_service.domain import ForecastedFile
from deepstroy_model_service.domain.data_access_layer.session import session
from deepstroy_model_service.helpers.s3_helper import S3Helper
import pandas as pd
import numpy as np
from io import StringIO

from deepstroy_model_service.helpers.s3_paths import create_path_for_file_forecasted


class NewPredictCommand:
    def __init__(self):
        pass

    def create(self, file_id, file_bytes, result):
        with open("data_tmp_file.xlsx", "wb") as binary_file:
            binary_file.write(file_bytes)
        df = pd.read_excel("data_tmp_file.xlsx")
        df["predicting_result"] = pd.Series(result)
        byte = df.to_csv(None).encode()
        forecasted_file_entity = ForecastedFile(
            id=file_id,
            path=create_path_for_file_forecasted()
        )
        S3Helper().s3_upload_file(
            file_path_in_bucket=forecasted_file_entity.path,
            file_bytes=byte,
            public=True,
        )
        current_session = session()
        try:
            current_session.add(forecasted_file_entity)
            current_session.commit()
            return forecasted_file_entity.id
        finally:
            current_session.close()
