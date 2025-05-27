import h5py
import datetime
import os


def __current_time(pattern='%Y/%m/%d %H:%M:%S'):
    return datetime.datetime.now().strftime(pattern)


def print_hierarchy(print_test):
    print(f"{print_test}:\t {__current_time()}")


def __get_proj_path():
    cur_path = os.path.abspath(os.path.dirname(__file__))
    proj_path = cur_path[:cur_path.find('src')]
    return proj_path


def __get_path(get_type: str, get_record: str):
    new_path = __get_proj_path() + '/' + get_type
    os.makedirs(new_path, exist_ok=True)
    new_path += ('/' + get_record)
    os.makedirs(new_path, exist_ok=True)
    return new_path


def get_result_path(get_record: str):
    return __get_path("result", get_record)


def try_to_find(dirname: str, filename: str) -> bool:
    temp = __get_proj_path()
    filenames = os.listdir(temp)
    if "data" in filenames:
        temp += '/' + "data"
        filenames = os.listdir(temp)
        if dirname in filenames:
            temp += '/' + dirname
            filenames = os.listdir(temp)
            if filename + ".h5" in filenames:
                return True
    return False


def read_data(dirname: str, filename: str) -> dict:
    dirname = __get_path("data", dirname)
    dirname += "/"
    with h5py.File(dirname + filename + '.h5', 'r') as f:
        data = dict()
        for i in f:
            data[i] = f[i][()]
    return data


def write_data(data_dict: dict, dirname: str, filename: str):
    dirname = __get_path("data", dirname)
    dirname += "/"
    with h5py.File(dirname + filename + '.h5', 'w') as f:
        for data_key in data_dict.keys():
            f.create_dataset(data_key, data=data_dict[data_key])
