""" Abstract Server process for various servers with Sigma-Rho envelopes """

from abc import abstractmethod
from Servers.Server import Server
from UD_Exceptions import ParameterOutOfBounds
from math import exp


class ServerDistribution(Server):

    @abstractmethod
    def sigma(self, theta: float) -> float:
        """ theta: MGF parameter """
        pass

    @abstractmethod
    def rho(self, theta: float) -> float:
        """ theta: MGF parameter """
        pass

    @abstractmethod
    def avg_rate(self, theta: float) -> float:
        pass

    def transient_bound(self, theta: float, delta_time: float) -> float:

        if theta <= 0:
            raise ParameterOutOfBounds(f"Theta value should be greater than 0")

        elif delta_time < 0:
            raise ValueError(f"Time value is always positive")

        return exp(theta * (-self.rho(theta) * delta_time + self.sigma(theta)))
