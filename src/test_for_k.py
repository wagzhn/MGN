import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from src.model import Model
from src.utils import *
from src.paras import a0
from itertools import product

# MODEL_NUM in src.paras must be "cerebellum"

RESULT_PATH = get_result_path("test_for_k")
RESULT_PATH += "/1"
os.makedirs(RESULT_PATH, exist_ok=True)


def plot_res(eps01_list, t_show, sol_list, k1, k2, k3, k4, tag):
    fig = plt.figure(figsize=(8, 6))
    gs = GridSpec(len(eps01_list), 4, figure=fig)
    for i in range(len(eps01_list)):
        ax1 = fig.add_subplot(gs[i, 0])
        ax1.set_title("$\epsilon_{01}$" + f"={eps01_list[i]:.2f}")
        ax1.plot(sol_list[i][0, :], sol_list[i][1, :])
        ax1.set_xlabel("$A_1$")
        ax1.set_ylabel("$A_2$")
        ax2 = fig.add_subplot(gs[i, 1:])
        for j in range(len(sol_list[i])):
            ax2.plot(t_show, sol_list[i][j, :], label=f"$A_{j + 1}$")
        ax2.set_xlabel("$t$")
        ax2.legend(loc='upper right')
        ax2.set_title(f"k1={k1}, k2={k2}, k3={k3}, k4={k4}")
    plt.tight_layout()
    plt.savefig(f"{RESULT_PATH}/{tag}.png")
    plt.close()


if __name__ == "__main__":
    k = lambda k1, k2, k3, k4: np.array([[0, -1, -7, k1],
                                         [1, 0, 0, k2],
                                         [23, 0, 0, 0],
                                         [k3, k4, 0, 0]])
    eps01_list = (1, 1.5, 2)
    tmax = 1000
    t_calc = (0, tmax)
    t_show = np.arange(tmax - 100, tmax, 0.01)
    ki_range = np.arange(-10, 11, 2)
    list_of_res = "".join(os.listdir(RESULT_PATH)).split(".png")[:-1]
    if len(list_of_res) == 0:
        already_save_tag = 0
    else:
        list_of_res = [int(i) for i in list_of_res]
        already_save_tag = max(list_of_res)

    tag = 0
    for k1, k2, k3, k4 in product(ki_range, repeat=4):
        tag += 1
        if tag <= already_save_tag: continue
        try:
            model = Model(k(k1, k2, k3, k4))
            sol_list = []
            for eps01 in eps01_list:
                sol_list.append(model.solve(a0, eps01, t_calc, t_show))
            plot_res(eps01_list, t_show, sol_list, k1, k2, k3, k4, tag)
            print(f"{tag}\t of {len(ki_range) ** 4}\t is done.")
        except:
            continue
