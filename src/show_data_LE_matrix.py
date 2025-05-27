from src.paras import *
from src.utils import *
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.interpolate import RegularGridInterpolator

DATA_PATH = "data_LE_matrix"
RESULT_PATH = get_result_path("LE_matrix")


def get_model_info(para_2, para_2_num):
    info = calc_dict[para_2]
    filename = ("le_matrix_data_" + para_2 +
                ("0" if info["data_name_with_0"] else "")
                + str(para_2_num))
    para_2_name = info["para_2_name"](para_2_num)
    Model2 = info["model2"]
    return filename, para_2_name, Model2


def get_data(filename):
    if try_to_find(DATA_PATH, filename):
        data = read_data(DATA_PATH, filename)
        para_2_list, eps01_list, le_matrix = data["para_2_list"], data["eps01_list"], data["le_matrix"]
    else:
        raise Exception("data is not found")
    return para_2_list, eps01_list, le_matrix


def plot_heatmap(para_2_list, eps01_list, le_matrix, para_2_name, step, filename):
    xticklabels = [f"{x:.3f}" if i % step == 0 else "" for i, x in enumerate(para_2_list)]
    yticklabels = [f"{x:.3f}" if i % step == 0 else "" for i, x in enumerate(eps01_list)]
    sns.heatmap(
        le_matrix,
        cmap="seismic",
        center=0,
        xticklabels=xticklabels,
        yticklabels=yticklabels
    )
    plt.tick_params(axis='both', which='both', length=0)
    plt.xticks(rotation=0)
    plt.xlabel(para_2_name)
    plt.ylabel("$\epsilon_{01}$")
    plt.title("LE in $\epsilon_{01}$-" + para_2_name + " plane")
    plt.tight_layout()
    plt.savefig(RESULT_PATH + "/" + filename.split("_")[-1] + ".png", dpi=200)
    # plt.savefig(RESULT_PATH + "/" + filename.split("_")[-1] + ".pdf")
    plt.close()


def plot_heatmap_smooth(para_2_list, eps01_list, le_matrix, para_2_name, step, filename):
    new_grid_factor = 10
    x = para_2_list
    y = eps01_list
    x_new = np.linspace(x[0], x[-1], len(x) * new_grid_factor)
    y_new = np.linspace(y[0], y[-1], len(y) * new_grid_factor)
    interp_func = RegularGridInterpolator((y, x), le_matrix, method='linear')
    xi_new, yi_new = np.meshgrid(x_new, y_new)
    points = np.array([yi_new.ravel(), xi_new.ravel()]).T
    le_matrix_smooth = interp_func(points).reshape(xi_new.shape)
    xticklabels_new = [f"{x:.3f}" if i % (step * new_grid_factor) == 0 else "" for i, x in enumerate(x_new)]
    yticklabels_new = [f"{x:.3f}" if i % (step * new_grid_factor) == 0 else "" for i, x in enumerate(y_new)]
    sns.heatmap(
        le_matrix_smooth,
        cmap="seismic",
        center=0,
        xticklabels=xticklabels_new,
        yticklabels=yticklabels_new
    )
    plt.tick_params(axis='both', which='both', length=0)
    plt.xticks(rotation=0)
    plt.xlabel(para_2_name)
    plt.ylabel("$\epsilon_{01}$")
    plt.title("LE in $\epsilon_{01}$-" + para_2_name + " plane")
    plt.tight_layout()
    plt.savefig(RESULT_PATH + "/" + filename.split("_")[-1] + "_smooth.png", dpi=200)
    # plt.savefig(RESULT_PATH + "/" + filename.split("_")[-1] + "_smooth.pdf")
    plt.close()


if __name__ == "__main__":
    step = 7
    for para_2 in calc_dict.keys():
        for para_2_num in calc_dict[para_2]["para_2_num"]:
            print_hierarchy(f"para {para_2}{para_2_num}")
            filename, para_2_name, _ = get_model_info(para_2, para_2_num)
            para_2_list, eps01_list, le_matrix = get_data(filename)
            # plot_heatmap(para_2_list, eps01_list, le_matrix, para_2_name, step, filename)
            plot_heatmap_smooth(para_2_list, eps01_list, le_matrix, para_2_name, step, filename)
