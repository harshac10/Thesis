""" Server Distribution Process with Sigma-Rho envelopes"""

from abc import ABC, abstractmethod
from math import exp


class ServerDistribution(ABC):

    @abstractmethod
    def sigma(self, theta: float) -> float:
        """ theta: MGF parameter"""
        pass

    @abstractmethod
    def rho(self, theta: float) -> float:
        """ theta: MGF parameter """
        pass

    @abstractmethod
    def avg_rate(self) -> float:
        pass

    def transient_bound(self, theta: float, delta_time: int) -> float:

        if theta <= 0:
            raise ValueError(f"Theta value must be greater than 0")

        elif delta_time < 0:
            raise ValueError(f"Delta time should always be positive")

        return exp(theta * (-self.rho(theta) * delta_time + self.sigma(theta)))
