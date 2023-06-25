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
    if obj_prg not in list(obj_prg_dict.keys()):
        obj_prg_dict[obj_prg] = obj_prg_dict[list(obj_prg_dict.keys())[-1]]+1

    return obj_prg_dict[str(obj_prg)]


def encode_obj_subprg(obj_subprg):
    if obj_subprg not in list(obj_subprg_dict.keys()):
        obj_subpr_dict[obj_subprg] = obj_subprg_dict[list(obj_subprg_dict.keys())[-1]] + 1

    return obj_subprg_dict[str(obj_subprg)]


def encode_obj_key(obj_key):
    obj_key_tmp = str(obj_key).replace('-', '')
    return int(obj_key_tmp)


def encode_code_task(code_task):
    code_task_tmp = str(code_task).replace('.', '')
    return int(code_task_tmp)


def str_to_date(string_date):
    # if type(string_date) is not Timestamp:
    #     return datetime.datetime.strptime(str(string_date), '%Y-%m-%d')
    pass

mean_dict = {
    'obj_prg': 0.6450463123664066,
    'obj_subprg': 1.9577141604399217,
    'obj_key': 30.831262217512833,
    'code_task': 595.8593620403018,
    'ПроцентЗавершенияЗадачи': 40.918263697316256,
    'estimated_task_time': 89.34964831832215,
}

std_dict = {
    'obj_prg': 0.47849972368091526,
    'obj_subprg': 1.0047899073201363,
    'obj_key': 18.494451983291594,
    'code_task': 356.15554933829293,
    'ПроцентЗавершенияЗадачи': 47.941105972527616,
    'estimated_task_time': 143.1226163826257,
}

def normalization(data):
    for colum in list(data.columns[:-1]):
        mean = mean_dict[colum]
        std = std_dict[colum]
        data[colum] = (data[colum]-mean)/std
    return data
