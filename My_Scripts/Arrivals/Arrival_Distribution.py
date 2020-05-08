""" Abstract Arrival process for various distribution with Sigma-Rho envelopes"""

from abc import abstractmethod, ABC
from math import exp


class ArrivalDistribution(ABC):

    @abstractmethod
    def sigma(self, theta: float) -> float:
        """ theta: MGF parameter"""
        pass

    @abstractmethod
    def rho(self, theta: float) -> float:
        """ theta: MGF parameter"""
        pass

    @abstractmethod
    def discrete(self) -> bool:
        """ True if the distribution is discrete else False"""
        pass

    @abstractmethod
    def mean_rate(self, theta: float) -> float:
        pass

    def transient_bound(self, theta: float, delta_time: int) -> float:

        if theta <= 0:
            raise ValueError(f"Theta value should be greater than 0")

        elif delta_time < 0:
            raise ValueError(f"Time values should always be positive")

        return exp(theta * (self.rho(theta) * delta_time + self.sigma(theta)))
