""" Token and Leaky Bucket Arrivals """

from abc import abstractmethod
from Arrivals.Arrival_Distribution import ArrivalDistribution
from UD_Exceptions import ParameterOutOfBounds
from math import exp, log


class RegulatedArrivals(ArrivalDistribution):

    def __init__(self, sigma_single=0.0, rho_single=0.0, n=1):
        self.sigma_single = sigma_single
        self.rho_single = rho_single
        self.n = n
        self.arr_rate = n * rho_single

    @abstractmethod
    def sigma(self, theta: float) -> float:
        pass

    def rho(self, theta: float) -> float:
        return self.arr_rate

    def discrete(self) -> bool:
        return True

    def mean_rate(self, theta: float) -> float:
        return self.rho(1.0)


class LeakyBucket(RegulatedArrivals):

    def __init__(self, sigma_single: float, rho_single: float, n=1):
        super().__init__(sigma_single= sigma_single, rho_single= rho_single, n=n)

    def sigma(self, theta: float) -> float:

        if theta <= 0:
            raise ParameterOutOfBounds(f"Theta value should be greater than 0")

        return self.n * log(0.5 * (exp(theta * self.sigma_single) + exp(-theta * self.sigma_single))) / theta


class TokenBucket(RegulatedArrivals):

    def __init__(self, sigma_single: float, rho_single: float, n=1):
        super().__init__(sigma_single= sigma_single, rho_single= rho_single, n=n)
        self.burst = self.n * self.sigma_single

    def sigma(self, theta: float) -> float:
        return self.n * self.sigma_single
