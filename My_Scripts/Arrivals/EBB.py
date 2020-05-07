""" Exponentially bounded Burst Arrivals """

from Arrivals.Arrival_Process import ArrivalDistribution
from math import log


class EBB(ArrivalDistribution):

    def __init__(self, m_factor: float, decay: float, rho_single: float, n=1):
        self.m_factor = m_factor
        self.decay = decay
        self.rho_single = rho_single
        self.n = n

    def sigma(self, theta: float) -> float:

        if theta <= 0:
            raise ValueError(f"Theta value should be greater than 0")

        elif self.m_factor < 0 or self.decay < 0:
            raise ValueError(f"M_factor and Decay value must be >= 0")

        elif self.decay <= theta:
            raise ValueError(f"Decay value should be greater than Theta")

        a = theta / self.decay
        log_part = log(self.m_factor ** a / (1 - a))
        return (log_part / theta) * self.n

    def rho(self, theta: float) -> float:

        if self.rho_single < 0:
            raise ValueError(f"Rho_Single must be >= 0")

        return self.n * self.rho_single

    def discrete(self) -> bool:
        return False

    def mean_rate(self, theta: float) -> float:
        return self.n * self.rho_single
