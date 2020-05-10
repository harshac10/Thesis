from Optimization.Setting import Setting
from scipy import optimize
from typing import List, Tuple
from math import inf
from UD_Exceptions import ParameterOutOfBounds
import numpy as np


class Optimize(object):

    def __init__(self, setting: Setting, num_of_param: int, print_x=True):
        self.setting = setting
        self.num_of_param = num_of_param
        self.print_x = print_x

    def evaluate_excep(self, param_list: List[float]) -> float:

        try:
            return self.setting.standard_bound(param_list)

        except(OverflowError, ParameterOutOfBounds, ValueError):
            return inf

    def grid_search(self, bound_list: List[Tuple[float,float]], delta: float) -> float:
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

        except FloatingPointError:
            return inf

        if self.print_x:
            print(f"Grid search optimal X: {grid_result[0].tolist()}")

        return grid_result[1]
