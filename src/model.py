import numpy as np
from scipy.integrate import solve_ivp
import multiprocessing as mp
from tqdm import tqdm
import math


class Model:
    def __init__(self, k):
        a_num = len(k)
        if a_num <= 1:
            raise Exception
        self.k = np.array(k, dtype=float)
        self.eps0 = np.array([1.0] * a_num)
        self.s = np.array([0.1] * a_num)
        self.p = np.array([4.0] * a_num)
        self.q = np.array([1.0] * a_num)
        self.d = np.array([0.1] * a_num)
        self.c = np.array([1.0] * a_num)
        self.epscrit = np.array([1.0] * a_num)

    def model(self, t, a):
        eps0 = self.eps0 + self.c * a
        return ((eps0 * self.s + np.dot(self.k, a) * self.q
                 * eps0 ** self.p / (eps0 ** self.p + self.epscrit ** self.p))
                * (1 - a) - self.d * a)

    def modify_paras(self, eps01):
        self.eps0[0] = eps01

    def solve(self, a0, eps01, t_calc, t_show):
        self.modify_paras(eps01)
        return solve_ivp(self.model, t_calc, a0, 'RK45', t_show, rtol=1e-8, atol=1e-8).y


class ModelCi(Model):
    def modify_paras(self, paras):
        self.eps0[0] = paras[0]
        self.c[paras[2]] = paras[1]


class ModelEps0i(Model):
    def modify_paras(self, paras):
        """
        paras: (eps01, eps0i, eps_num)
        """
        self.eps0[0] = paras[0]
        self.eps0[paras[2]] = paras[1]


class ModelKij(Model):
    def modify_paras(self, paras):
        self.eps0[0] = paras[0]
        self.k[paras[2] // 10, paras[2] % 10] = paras[1]


class ModelDi(Model):
    def modify_paras(self, paras):
        self.eps0[0] = paras[0]
        self.d[paras[2]] = paras[1]


class ModelSi(Model):
    def modify_paras(self, paras):
        self.eps0[0] = paras[0]
        self.s[paras[2]] = paras[1]


class ModelQi(Model):
    def modify_paras(self, paras):
        self.eps0[0] = paras[0]
        self.q[paras[2]] = paras[1]


class ModelEpscriti(Model):
    def modify_paras(self, paras):
        self.eps0[0] = paras[0]
        self.epscrit[paras[2]] = paras[1]


class LyapunovExponent:
    @staticmethod
    def get_y0(x0, d, seed):
        np.random.seed(seed)
        y0 = np.random.rand(len(x0))
        y0 = y0 / np.linalg.norm(y0)
        y0 *= d
        y0 += x0
        return y0

    def __init__(self, model: Model, x0, d, tau, m, seed=717):
        self.model = model
        self.x0 = x0
        self.d = d
        self.y0 = LyapunovExponent.get_y0(x0, d, seed)
        self.tau = tau
        self.m = m
        self.t_calc = np.arange(tau * 0.9, tau, 0.1)

    def calc_le(self, eps01):
        le = 0
        x0, y0 = self.x0, self.y0
        for i in range(self.m):
            sol1 = self.model.solve(x0, eps01, (0, self.tau), self.t_calc)
            sol2 = self.model.solve(y0, eps01, (0, self.tau), self.t_calc)
            dt_all = np.linalg.norm(sol1 - sol2, axis=0)
            x0 = sol1[:, -1]
            y0 = sol2[:, -1]
            direction = y0 - x0
            dt = dt_all[-1]
            unit_direction = direction / dt
            y0 = x0 + self.d * unit_direction
            le += math.log(np.min(dt_all) / self.d)
        le /= self.m * self.tau
        return le

    def calc_le_vals(self, eps01_list):
        cpu_count = min(36, mp.cpu_count())
        chunksize = 5
        with mp.Pool(processes=cpu_count) as pool:
            results = []
            for le in tqdm(pool.imap(self.calc_le, eps01_list, chunksize=chunksize), total=len(eps01_list)):
                results.append(le)
        return np.array(results)
