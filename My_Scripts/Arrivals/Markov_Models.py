""" Markov Model Arrivals for continuous and discrete time """

from Arrivals.Arrival_Distribution import ArrivalDistribution
from math import exp, log, sqrt


class MarkovModelCont(ArrivalDistribution):

    def __init__(self, lamda: float, mue: float, burst: float, n=1):
        self.lamda = lamda
        self.mue = mue
        self.burst = burst
        self.n = n

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:

        if theta <= 0:
            raise ValueError(f"Theta value should be greater than 0")

        a = theta * self.burst - self.lamda - self.mue
        return (self.n / 2 * theta) * (a + sqrt(a**2 + 4 * self.mue * theta * self.burst))

    def discrete(self) -> bool:
        return False

    def mean_rate(self, theta: float) -> float:
        return self.mue / (self.mue + self.lamda) * self.burst


class MarkovModelDisc(ArrivalDistribution):

    def __init__(self, on: float, off: float, burst: float, n=1):
        self.on = on
        self.off = off
        self.burst = burst
        self.n = n

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:

        if theta <= 0:
            raise ValueError(f"Theta value should be greater than 0")

        a = self.on + self.off * exp(theta * self.burst)
        log_part = log(a + sqrt(a**2 - 4 * (self.off + self.on - 1) * exp(theta * self.burst)) / 2)
        return self.n * log_part / theta

    def discrete(self) -> bool:
        return True

    def mean_rate(self, theta: float) -> float:
        return self.n * (1 - self.off) / (2 - self.off - self.on) * self.burst

