from abc import ABC
import datetime

from sklearn.model_selection import train_test_split
import numpy as np
from imblearn.over_sampling import SMOTE
import pandas as pd
import joblib

from deepstroy_model_service.base.processing_model_base import ProcessingModelBase
from deepstroy_model_service.helpers.data_parsing_helper import encode_obj_prg, encode_obj_subprg, encode_obj_key, \
    encode_code_task, str_to_date, normalization, std_dict, mean_dict


class ForecastingModel(ProcessingModelBase, ABC):
    def __init__(self):
        super().__init__()

    def process_data(self, bytes_data):
        with open("data_tmp_file.xlsx", "wb") as binary_file:
            binary_file.write(bytes_data)
        test_data = pd.read_excel("data_tmp_file.xlsx")
        test_data = test_data.drop(labels=[test_data.columns[0], 'obj_pwa_key', 'obj_shortName', 'НазваниеЗадачи',
                                           'Статуспоэкспертизе', 'Экспертиза'],
                                   errors='ignore',
                                   axis=1)

        test_data = test_data.rename(columns={"ДатаначалаБП0": "bpo_start_date",
                                      "ДатаокончанияБП0": "bpo_end_date",
                                      "Кодзадачи": "code_task"})
        test_data.obj_prg = test_data.obj_prg.apply(encode_obj_prg)
        test_data.obj_subprg = test_data.obj_subprg.apply(encode_obj_prg)
        test_data.obj_key = test_data.obj_key.apply(encode_obj_key)
        test_data.code_task = test_data.code_task.apply(encode_code_task)

        if 'ДатаНачалаЗадачи' in test_data.columns and 'ДатаОкончанияЗадачи' in test_data.columns:
            test_data = test_data.rename(
                columns={"ДатаНачалаЗадачи": "task_start_date", "ДатаОкончанияЗадачи": "task_end_date"})
            # test_data.task_start_date = test_data.task_start_date.apply(str_to_date)
            # test_data.task_end_date = test_data.task_end_date.apply(str_to_date)
            test_data.insert(len(test_data.columns), 'estimated_task_time',
                             list(test_data.task_end_date - test_data.task_start_date), False)

            test_data['estimated_task_time'] = pd.to_numeric(test_data['estimated_task_time'].dt.days,
                                                                downcast='integer')

        # test_data.bpo_start_date = test_data.bpo_start_date.apply(str_to_date)
        # test_data.bpo_end_date = test_data.bpo_end_date.apply(str_to_date)

        test_data.insert(len(test_data.columns), 'bpo_task_time',
                         list(test_data.bpo_end_date - test_data.bpo_start_date), False)

        test_data['bpo_task_time'] = pd.to_numeric(test_data['bpo_task_time'].dt.days,
                                                         downcast='integer')
        test_data = test_data.drop(labels=['task_start_date', 'task_end_date', 'bpo_start_date',
                                           'bpo_end_date'],
                                   errors='ignore',
                                   axis=1)

        normalized_data = normalization(test_data)

        model = joblib.load('model.pkl')

        # X_test = np.array(test_dataset[normalized_data.columns[:-2]])

        # if 'estimated_task_time' in test_data.columns:
        #     y_test = np.array(test_dataset[normalized_data.columns[-2:-1]]).flatten()
        #
        # pool_test = Pool(X_test, y_test)
        if 'estimated_task_time' in test_data.columns:
            X_test = np.array(test_data[normalized_data.columns[:-2]])
            print(f'With estimated_task_time: {X_test[0]}')
            answer = model.predict(X_test)
            answer = (answer + mean_dict['estimated_task_time']) * std_dict['estimated_task_time']
        else:
            X_test = np.array(test_data[normalized_data.columns[:-1]])
            print(f'NOT estimated_task_time: {X_test[0]}')
            answer = model.predict(X_test)
            answer = (answer + mean_dict['estimated_task_time']) * std_dict['estimated_task_time']

        print(answer)

        # return array with results
