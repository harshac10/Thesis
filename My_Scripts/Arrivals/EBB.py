""" Exponentially Bounded Burst """

from Arrivals.Arrival_Distribution import ArrivalDistribution
from UD_Exceptions import ParameterOutOfBounds
from math import log


class ExpBoundBurst(ArrivalDistribution):

    def __init__(self, m_factor: float, decay: float, rho_single: float, n=1):
        self.m_fac = m_factor
        self.decay = decay
        self.rho_val = rho_single
        self.n = n

    def sigma(self, theta: float) -> float:

        if theta <= 0:
            raise ParameterOutOfBounds(f"Theta value should be greater than 0")

        elif self.m_fac < 0 or self.decay < 0 or self.rho_val < 0:
            raise ValueError(f"M_factor, Decay and Rho values should be positive")

        elif self.decay <= theta:
            raise ValueError(f"Decay value should be greater than theta")

        a = theta / self.decay
        log_part = log(self.m_fac ** a / (1 - a))

        if log_part < 0:
            raise ParameterOutOfBounds("Rhos must be >= 0")

        return log_part / theta * self.n

    def rho(self, theta: float) -> float:
        return self.n * self.rho_val

    def discrete(self) -> bool:
        return False

    def mean_rate(self, theta: float) -> float:
        return self.n * self.rho_val
