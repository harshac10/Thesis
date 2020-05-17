from Optimize.Setting import Setting
from scipy import optimize
from typing import List, Tuple, Union
from math import inf
from UD_Exceptions import ParameterOutOfBounds
import numpy as np


class Optimize(object):

    def __init__(self, setting: Setting, num_of_param: int):
        self.setting = setting
        self.num_of_param = num_of_param

    def evaluate_excep(self, param_list: List[float]) -> float:

        try:
            return self.setting.standard_bound(param_list)

        except(OverflowError, ParameterOutOfBounds, ValueError):
            return inf

    def grid_search(self, bound_list: List[Tuple[float,float]], delta: float):
        """ Grid search approach using brute force optimization
        *bound_list -> list of tuples with lower and upper bounds
        *delta -> granularity of search
        """

        if len(bound_list) != self.num_of_param:
            raise ParameterOutOfBounds(f"Number of parameters are wrong")

        list_slices = [slice(0)] * len(bound_list)
        for i in range(len(bound_list)):
            list_slices[i] = slice(bound_list[i][0], bound_list[i][1], delta)

        np.seterr("raise")

        try:
            grid_result = optimize.brute(func= self.evaluate_excep, ranges= tuple(list_slices), full_output= True)
            return grid_result[0][0], grid_result[1]

        except FloatingPointError:
            return inf, inf

    def nelder_mead(self, simplex: np.ndarray, sd_min = 10**-2):

        np.seterr("raise")
        try:
            nm_result = optimize.minimize(fun=self.evaluate_excep, x0=np.zeros(shape=(1,simplex.shape[1])),
                                          method='Nelder-Mead', options={'fatol': sd_min})

            return nm_result.x[0], nm_result.fun

        except FloatingPointError:
            return inf, inf

    def basin_hopping(self, start_list: List[float]):

        np.seterr("raise")

        try:
            bh_result = optimize.basinhopping(func= self.evaluate_excep, x0= start_list)
            return bh_result.x[0], bh_result.fun

        except FloatingPointError:
            return inf, inf

    def diff_evolution(self, bound_list: List[tuple]):

        np.seterr("raise")

        try:
            de_result = optimize.differential_evolution(func= self.evaluate_excep, bounds= bound_list)
            return de_result.x[0], de_result.fun

        except FloatingPointError:
            return inf, inf

    def dual_annealing(self, bound_list: List[tuple]):

        np.seterr("raise")

        try:
            da_result = optimize.dual_annealing(func= self.evaluate_excep,bounds= bound_list)
            return da_result.x[0], da_result.fun

        except FloatingPointError:
            return inf, inf


