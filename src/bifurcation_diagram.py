import matplotlib.pyplot as plt
from src.paras import *
from src.utils import *

DATA_PATH = "data_bifurcation"
RESULT_PATH = get_result_path("bifurcation_diagram")


def poincare_bifurcation(sol, poincare_plane_axis, poincare_plane_val, save_axis):
    sol_sgn = sol[poincare_plane_axis, :] > poincare_plane_val
    sol_index = np.where(sol_sgn[:-1] & ~sol_sgn[1:])[0]
    sol_i0 = sol[:, sol_index]
    sol_i1 = sol[:, sol_index + 1]
    plane0 = sol_i0[poincare_plane_axis, :]
    plane1 = sol_i1[poincare_plane_axis, :]
    t_i = (poincare_plane_val - plane0) / (plane1 - plane0)
    val_interp = (1 - t_i) * sol_i0[save_axis, :] + t_i * sol_i1[save_axis, :]
    return val_interp


def plot_bifurcation(eps01_vals, vals, plt_title):
    plt.figure(figsize=(8, 6))
    plt.scatter(eps01_vals, vals, color='black', s=0.1, edgecolors='none')
    plt.xlabel("$\epsilon_{01}$")
    plt.ylabel("$A_2$")
    plt.title(plt_title)
    plt.tight_layout()
    plt.savefig(RESULT_PATH + "/" + plt_title + ".pdf")
    plt.close()


if __name__ == "__main__":
    if MODEL_NUM == "original":
        filename = "bifurcation_data_sub3"
        plt_title = "3-subnetwork model"
        eps01_list = np.arange(1.39, 1.45, 0.00003)
    elif MODEL_NUM == "cerebellum":
        filename = "bifurcation_data_sub4"
        plt_title = "4-subnetwork model"
        eps01_list = np.arange(1.466, 1.666, 0.0001)
    else:
        raise Exception

    if try_to_find(DATA_PATH, filename):
        data = read_data(DATA_PATH, filename)
        eps01_vals, vals = data["eps01_vals"], data["vals"]
    else:
        model = Model(k)
        poincare_plane_axis = 0
        poincare_plane_val = 0
        save_axis = 1
        assert poincare_plane_axis != save_axis
        eps01_vals = []
        vals = []
        for eps01 in tqdm(eps01_list):
            sol = model.solve(a0, eps01, t_calc, t_show)
            val_interp = poincare_bifurcation(sol, poincare_plane_axis, poincare_plane_val, save_axis)
            eps01_vals.extend([eps01] * len(val_interp))
            vals.extend(val_interp)
        write_data({"eps01_vals": eps01_vals, "vals": vals},
                   DATA_PATH, filename)
    plot_bifurcation(eps01_vals, vals, plt_title)
