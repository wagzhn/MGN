from itertools import product
import matplotlib.pyplot as plt
from matplotlib import gridspec
from utils import *
from src.paras import *

DATA_PATH = "data_LE"
RESULT_PATH = get_result_path("LE")


def plot_arrow(start_x, end_x, y_level, text, text2):
    plt.annotate('', xy=(start_x, y_level), xytext=(end_x, y_level),
                 arrowprops=dict(arrowstyle='<->', color='red', lw=1.5))
    plt.text((start_x + end_x) / 2, y_level + 0.002, text, ha='center', fontsize=12, color='red')
    plt.text((start_x + end_x) / 2, y_level - 0.005, f"({text2})", ha='center', fontsize=10, color='red')


def plot_le(eps01_list, le_vals, x_num):
    if x_num == 1:
        if MODEL_NUM == "original":
            plot_arrow(1.39, 1.4006, 0.05, "P-MLE", "inter-ictal")
            plt.axvline(1.4006, color='red', linestyle='--', linewidth=1)
            plot_arrow(1.4006, 1.4253, 0.05, "N-MLE", "prodromal")
            plt.axvline(1.4253, color='red', linestyle='--', linewidth=1)
            plot_arrow(1.4253, 1.45, 0.05, "P-MLE", "ictal")
            plt.plot(eps01_list, le_vals, '-', markersize=1)
            plt.xlim([eps01_list[0], eps01_list[-1]])
            plt.ylim([-0.02, 0.06])
        elif MODEL_NUM == "cerebellum":
            plot_arrow(1.466, 1.5015, 0.05, "SP-MLE", "inter-ictal")
            plt.axvline(1.5015, color='red', linestyle='--', linewidth=1)
            plot_arrow(1.5015, 1.531, 0.05, "N-MLE", "prodromal")
            plt.axvline(1.531, color='red', linestyle='--', linewidth=1)
            plot_arrow(1.531, 1.627, 0.05, "ZF-MLE", "aura")
            plt.axvline(1.627, color='red', linestyle='--', linewidth=1)
            plot_arrow(1.627, 1.666, 0.05, "LP-MLE", "ictal")
            plt.plot(eps01_list, le_vals, '-', markersize=1)
            plt.xlim([eps01_list[0], eps01_list[-1]])
            plt.ylim([-0.02, 0.06])
    plt.plot(eps01_list, le_vals, '-', color="#1f77b4", markersize=1)
    plt.xlim([eps01_list[0], eps01_list[-1]])
    plt.axhline(0, color='gray', linestyle='--', linewidth=1)
    plt.ylabel("Lyapunov exponent")
    plt.xticks([])


def plot_var_strip(eps01_list, le_vals, x_num):
    window_size = 5
    local_variances = np.zeros(len(le_vals) - 2 * window_size)
    for i in range(len(local_variances)):
        window = le_vals[i:i + window_size * 2 + 1]
        local_variances[i] = np.std(window)
    y = np.zeros(len(le_vals))
    y[window_size:-window_size] = local_variances
    le_strip = np.tile(y, (10, 1))
    extent = [eps01_list[0], eps01_list[-1], 0, 1]
    vmax = np.max(np.abs(y))
    plt.imshow(le_strip, cmap='seismic', extent=extent, origin='lower',
               aspect='auto', norm=plt.Normalize(vmin=-vmax, vmax=vmax))
    plt.yticks([])
    plt.xlabel("$\epsilon_{0" + str(x_num) + "}$")


def plot_le_strip(eps01_list, le_vals):
    le_strip = np.tile(le_vals, (10, 1))
    extent = [eps01_list[0], eps01_list[-1], 0, 1]
    vmax = np.max(np.abs(le_vals))
    plt.imshow(le_strip, cmap='seismic', extent=extent, origin='lower',
               aspect='auto', norm=plt.Normalize(vmin=-vmax, vmax=vmax))
    plt.xticks([])
    plt.yticks([])


def plot_res(eps01_list, le_vals, plt_title, save_name=None, x_num=1):
    if save_name is None:
        save_name = plt_title
    plt.figure(figsize=(8, 6))
    gs = gridspec.GridSpec(3, 1, height_ratios=[4, 0.5, 0.5])
    plt.subplot(gs[0])
    plot_le(eps01_list, le_vals, x_num)
    plt.subplot(gs[1])
    plot_le_strip(eps01_list, le_vals)
    plt.subplot(gs[2])
    plot_var_strip(eps01_list, le_vals, x_num)
    plt.suptitle(plt_title)
    plt.tight_layout()
    plt.savefig(RESULT_PATH + "/" + save_name + ".png", dpi=1000)
    plt.savefig(RESULT_PATH + "/" + save_name + ".pdf")
    plt.close()


if __name__ == "__main__":
    if MODEL_NUM == "original":
        filename = "le_data_sub3"
        plt_title = "3-subnetwork model"
        eps01_list = np.arange(1.39, 1.45, 0.00003)
    elif MODEL_NUM == "cerebellum":
        filename = "le_data_sub4"
        plt_title = "4-subnetwork model"
        eps01_list = np.arange(1.466, 1.666, 0.0001)
    else:
        raise Exception

    if try_to_find(DATA_PATH, filename):
        data = read_data(DATA_PATH, filename)
        eps01_list, le_vals = data["eps01_list"], data["le_vals"]
    else:
        model = Model(k)
        LE_calc = LyapunovExponent(model, x0=a0, d=1e-4, tau=200, m=10)
        le_vals = LE_calc.calc_le_vals(eps01_list=eps01_list)
        write_data({"eps01_list": eps01_list, "le_vals": le_vals},
                   DATA_PATH, filename)
    plot_res(eps01_list, le_vals, plt_title)

    eps04_list = np.arange(0.99, 1.01, 0.00001)
    eps01 = 1.549
    filename = "le_data_sub4_eps04"
    plt_title = "4-subnetwork model with the variation of $\epsilon_{04}$ ($\epsilon_{01}$ = " + f"{eps01} )"
    if try_to_find(DATA_PATH, filename):
        data = read_data(DATA_PATH, filename)
        eps04_list, le_vals = data["eps04_list"], data["le_vals"]
    else:
        model = ModelEps0i(k)
        LE_calc = LyapunovExponent(model, x0=a0, d=1e-4, tau=200, m=10)
        iter_list = list(product((eps01,), eps04_list, (4,)))
        le_vals = LE_calc.calc_le_vals(iter_list)
        write_data({"eps04_list": eps04_list, "le_vals": le_vals},
                   DATA_PATH, filename)
    plot_res(eps04_list, le_vals, plt_title, "4-subnetwork model (eps04)", x_num=4)
