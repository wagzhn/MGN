from src.paras import *
from src.utils import *
from itertools import product

DATA_PATH = "data_LE_matrix"


def get_model_info(para_2, para_2_num):
    info = calc_dict[para_2]
    filename = ("le_matrix_data_" + para_2 +
                ("0" if info["data_name_with_0"] else "")
                + str(para_2_num))
    para_2_name = info["para_2_name"](para_2_num)
    Model2 = info["model2"]
    return filename, para_2_name, Model2


def get_data(filename, Model2, delta_para_2, para_2, para_2_num, test_factor):
    if not try_to_find(DATA_PATH, filename):
        model = Model2(k)
        LE_calc = LyapunovExponent(model, x0=a0, d=1e-4, tau=200, m=10)
        if para_2 == "k":
            para_2_num -= 11
            p1, p2 = para_2_num // 10, para_2_num % 10
            para_2_val = eval(f"model.{para_2}[{p1},{p2}]")
        else:
            para_2_num -= 1
            para_2_val = eval(f"model.{para_2}[{para_2_num}]")
        grid_size = delta_para_2 * 0.03 * test_factor
        para_2_list = np.arange(para_2_val - delta_para_2, para_2_val + delta_para_2 + grid_size / 10, grid_size)
        eps01_list = np.arange(1.466, 1.666 + 0.003 * test_factor / 10, 0.003 * test_factor)
        iter_list = list(product(eps01_list, para_2_list, (para_2_num,)))
        le_matrix = LE_calc.calc_le_vals(iter_list)
        le_matrix = le_matrix.reshape((len(eps01_list), len(para_2_list)))
        write_data({"para_2_list": para_2_list, "eps01_list": eps01_list, "le_matrix": le_matrix},
                   DATA_PATH, filename)


if __name__ == "__main__":
    test_factor = 1
    for para_2 in calc_dict.keys():
        for para_2_num in calc_dict[para_2]["para_2_num"]:
            delta_para_2 = calc_dict[para_2]["delta_para_2"]
            print_hierarchy(f"para {para_2}{para_2_num}")
            filename, _, Model2 = get_model_info(para_2, para_2_num)
            get_data(filename, Model2, delta_para_2, para_2, para_2_num, test_factor)
