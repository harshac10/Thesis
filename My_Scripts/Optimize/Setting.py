""" Abstract class for obtaining bounds for Topologies """

from abc import abstractmethod
from typing import List


class Setting(object):

    @abstractmethod
    def standard_bound(self, param_list: List[float]) -> float:
        """ Theta and Hoelder´s parameters """
        pass

    @abstractmethod
    def approx_util(self) -> float:
        pass
