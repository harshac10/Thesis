""" Arrivals based on Queuing theory """

from Arrivals.Arrival_Distribution import ArrivalDistribution
from UD_Exceptions import ParameterOutOfBounds
from math import exp, log


class DM1(ArrivalDistribution):

    def __init__(self, lamda: float, n=1):
        self.lamda = lamda
        self.n = n

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:

        if theta <= 0:
            raise ParameterOutOfBounds(f"Theta value should be greater than 0")

        elif self.lamda <= theta:
            raise ValueError(f"Lambda value should be greater than theta")

        return (self.n / theta) * log(self.lamda / (self.lamda - theta))

    def discrete(self) -> bool:
        return True

    def mean_rate(self, theta: float) -> float:
        return self.n / self.lamda


class MD1(ArrivalDistribution):

    def __init__(self, lamda: float, mue: float, n=1):
        self.lamda = lamda
        self.mue = mue
        self.n = n

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:

        if theta <= 0:
            raise ParameterOutOfBounds(f"Theta value should be greater than 0")

        return self.n * self.lamda / theta * (exp(theta / self.mue) - 1)

    def discrete(self) -> bool:
        return False

    def mean_rate(self, theta: float) -> float:
        return self.n * self.lamda / self.mue


class MM1(ArrivalDistribution):

    def __init__(self, lamda: float, mue: float, n=1):
        self.lamda = lamda
        self.mue = mue
        self.n = n

    def sigma(self, theta: float) -> float:
        return 0.0

    def rho(self, theta: float) -> float:

        if theta <= 0:
            raise ParameterOutOfBounds(f"Theta value should be greater than 0")

        elif self.mue <= theta:
            raise ParameterOutOfBounds(f"Mue value should be greater than theta")

        return self.n * self.lamda / (self.mue - theta)

    def discrete(self) -> bool:
        return False

    def mean_rate(self, theta: float) -> float:
        return self.n * self.lamda / self.mue
