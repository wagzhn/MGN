from model import *

"""
MODEL_NUM = "original"
3-sub model (original)

MODEL_NUM = "cerebellum"
4-sub model (cerebellum)
"""

MODEL_NUM = "cerebellum"

tmax = 2000
t_calc = (0, tmax)
t_show = np.arange(tmax - 300, tmax, 0.01)

if MODEL_NUM == "original":
    a0 = np.array([0.59, -7.9, 0.99])
    k = np.array([[0, -1, -7],
                  [1, 0, 0],
                  [23, 0, 0]])
    eps01_list = np.arange(1.39, 1.45, 1e-4)
elif MODEL_NUM == "cerebellum":
    a0 = np.array([0.59, -7.9, 0.99, -1])
    k = np.array([[0, -1, -7, -6],
                  [1, 0, 0, -4],
                  [23, 0, 0, 0],
                  [-8, 6, 0, 0]])
    eps01_list = np.arange(1.466, 1.666, 1e-3)
else:
    raise Exception

calc_dict = {
    "eps": {"para_2_num": (2, 3, 4), "delta_para_2": 0.01,
            "model2": ModelEps0i, "data_name_with_0": True, "para_2_num_minus": 1,
            "para_2_name": lambda para_2_num: "$\epsilon_{0" + f"{para_2_num}" + "}$"},
    "c": {"para_2_num": (1, 2, 3, 4), "delta_para_2": 0.1,
          "model2": ModelCi, "data_name_with_0": False, "para_2_num_minus": 1,
          "para_2_name": lambda para_2_num: f"$c_{para_2_num}$"},
    "k": {"para_2_num": (12, 13, 14, 21, 24, 31, 41, 42), "delta_para_2": 0.1,
          "model2": ModelKij, "data_name_with_0": False, "para_2_num_minus": 11,
          "para_2_name": lambda para_2_num: "$k_{" + f"{para_2_num}" + "}$"},
    "d": {"para_2_num": (1, 2, 3, 4), "delta_para_2": 0.01,
          "model2": ModelDi, "data_name_with_0": False, "para_2_num_minus": 1,
          "para_2_name": lambda para_2_num: f"$d_{para_2_num}$"},
    "s": {"para_2_num": (1, 2, 3, 4), "delta_para_2": 0.01,
          "model2": ModelSi, "data_name_with_0": False, "para_2_num_minus": 1,
          "para_2_name": lambda para_2_num: f"$S_{para_2_num}$"},
    "q": {"para_2_num": (1, 2, 3, 4), "delta_para_2": 0.1,
          "model2": ModelQi, "data_name_with_0": False, "para_2_num_minus": 1,
          "para_2_name": lambda para_2_num: f"$q_{para_2_num}$"},
    "epscrit": {"para_2_num": (1, 2, 3, 4), "delta_para_2": 0.1,
                "model2": ModelEpscriti, "data_name_with_0": True, "para_2_num_minus": 1,
                "para_2_name": lambda para_2_num: "$\epsilon_{crit" + f"{para_2_num}" + "}$"},
}
