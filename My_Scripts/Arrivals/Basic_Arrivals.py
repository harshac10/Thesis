""" Standard Arrival distributions """

from Arrivals.Arrival_Distribution import ArrivalDistribution
from UD_Exceptions import ParameterOutOfBounds
from math import exp, log


class Bernoulli(ArrivalDistribution):

    def __init__(self, p_val: float, n=1):
        self.p_val = p_val
        self.n = n

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:

        if theta <= 0:
            raise ParameterOutOfBounds(f"Theta value should be greater than 0")

        return (self.n / theta) * log(1 - self.p_val + (self.p_val * exp(theta)))

    def discrete(self) -> bool:
        return True

    def mean_rate(self, theta: float) -> float:
        return self.p_val * self.n


class Poisson(ArrivalDistribution):

    def __init__(self, lamda: float, n=1):
        self.lamda = lamda
        self.n = n

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:

        if theta <= 0:
            raise ParameterOutOfBounds(f"Theta value should be greater than 0")

        return (self.n / theta) * self.lamda * (exp(theta) - 1)

    def discrete(self) -> bool:
        return True

    def mean_rate(self, theta: float) -> float:
        return self.lamda


class Uniform(ArrivalDistribution):

    def __init__(self, n=1):
        self.n = n

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:

        if theta <= 0:
            raise ParameterOutOfBounds(f"Theta value should be greater than 0")

        return self.n - (self.n * log(theta) / theta)

    def discrete(self) -> bool:
        return False

    def mean_rate(self, theta: float) -> float:
        return self.n / 2
