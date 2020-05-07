""" Markov Model Arrivals for Continuous and Discrete(On-Off Model) time """

from Arrivals.Arrival_Process import ArrivalDistribution
from math import sqrt, log, exp


class MarkovModelCont(ArrivalDistribution):
    """ Continuous time """

    def __init__(self, lamda: float, mue: float, burst: float, n=1):
        self.lamda = lamda
        self.mue = mue
        self.burst = burst
        self.n = n

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:
        if theta <= 0:
            raise ValueError(f"Theta value must be greater than 0")

        a = theta * self.burst - self.mue - self.lamda
        return (self.n / (2 * theta)) * (a + sqrt(a**2 + 4*self.mue*theta*self.burst))

    def discrete(self) -> bool:
        return False

    def mean_rate(self, theta: float) -> float:
        a = self.mue / (self.mue + self.lamda)
        return a * self.burst


class MarkovModelDisc(ArrivalDistribution):
    """ Discrete time """

    def __init__(self, on: float, off: float, burst: float, n=1):
        self.on = on
        self.off = off
        self.burst = burst
        self.n = n

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:

        if theta <= 0:
            raise ValueError(f"Theta value must be greater than 0")

        a = self.off + self.on * exp(theta * self.burst)
        log_part = log(a + sqrt(a**2 - 4*(self.on + self.off - 1) * exp(theta * self.burst)) / 2)
        return (self.n / theta) * log_part

    def discrete(self) -> bool:
        return True

    def mean_rate(self, theta: float) -> float:
        return self.n * (1 - self.off) / (2 - self.off - self.on) * self.burst
