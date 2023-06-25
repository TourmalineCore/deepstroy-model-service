from deepstroy_model_service.domain import ForecastedFile
from deepstroy_model_service.domain.data_access_layer.session import session
from deepstroy_model_service.helpers.s3_helper import S3Helper
import pandas as pd
import numpy as np
from io import StringIO

import datetime
from deepstroy_model_service.helpers.s3_paths import create_path_for_file_forecasted


class NewPredictCommand:
    def __init__(self):
        pass

    def create(self, file_id, file_bytes, result):
        with open("data_tmp_file.xlsx", "wb") as binary_file:
            binary_file.write(file_bytes)
        df = pd.read_excel("data_tmp_file.xlsx")
        df["Кол-во дней"] = np.nan

        df['ДатаокончанияБП0'] = pd.to_datetime(df['ДатаокончанияБП0'], format='%Y-%m-%d')
        df['ДатаначалаБП0'] = pd.to_datetime(df['ДатаначалаБП0'], format='%Y-%m-%d')

        for index, row in df.iterrows():
            df["Кол-во дней"][index] = pd.Series((row['ДатаокончанияБП0'] - (row['ДатаначалаБП0'] + datetime.timedelta(days=int(result[index]))).days))

        print(df["Кол-во дней"])

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
