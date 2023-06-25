import datetime

obj_prg_dict = {
    'Образование': 0,
    'Здравоохранение': 1
}

obj_subprg_dict = {
    'Дошкольные учреждения': 0,
    'Общеобразовательные учреждения': 1,
    'ССК': 2,
    'Поликлиники': 3
}


def encode_obj_prg(obj_prg):
    if type(obj_prg) != str:
        return 0

    if obj_prg not in list(obj_prg_dict.keys()):
        obj_prg_dict[obj_prg] = obj_prg_dict[list(obj_prg_dict.keys())[-1]] + 1

    return obj_prg_dict[str(obj_prg)]


def encode_obj_subprg(obj_subprg):
    if type(obj_subprg) != str:
        return 0

    if obj_subprg not in list(obj_subprg_dict.keys()):
        obj_subprg_dict[obj_subprg] = obj_subprg_dict[list(obj_subprg_dict.keys())[-1]] + 1

    return obj_subprg_dict[str(obj_subprg)]


def encode_obj_key(obj_key):
    if type(obj_key) != str:
        return int('020-0684'.replace('-', ''))

    obj_key_tmp = str(obj_key).replace('-', '')
    return int(obj_key_tmp)


def encode_code_task(code_task):
    if type(code_task) != str:
        return 1

    code_task_tmp = str(code_task).replace('.', '')
    return int(code_task_tmp)


def str_to_date(string_date):
    if type(string_date) is not str:
        return datetime.datetime.strptime('2023-06-25', '%Y-%m-%d')

    return datetime.datetime.strptime(str(string_date), '%Y-%m-%d')

mean_dict = {
    'obj_prg': 0.6450463123664066,
    'obj_subprg': 1.4494475432259544,
    'obj_key': 200072.6820076828,
    'code_task': 319491.7425404002,
    'ПроцентЗавершенияЗадачи': 49.46153142601284,
    'estimated_task_time': 91.31040508036355,
}

std_dict = {
    'obj_prg': 0.47849972368091526,
    'obj_subprg': 1.1244132623508827,
    'obj_key': 13020.893417773561,
    'code_task': 1871775.5762401205,
    'ПроцентЗавершенияЗадачи': 48.899172625499176,
    'estimated_task_time': 141.96508889870012,
}

def normalization(data):
    for colum in list(data.columns[:-1]):
        mean = mean_dict[colum]
        std = std_dict[colum]
        data[colum] = (data[colum]-mean)/std
    return data
