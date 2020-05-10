""" Implementing network operations with Sigma-Rho calculus """

from Arrivals.Arrival import Arrival
from Servers.Server import Server
from Performance_Bounds.Additional_Functions import sig_rho, get_q, stability_check, get_pn
from UD_Exceptions import ParameterOutOfBounds
from math import exp, log
from typing import List


class Deconvolve(Arrival):

    def __init__(self, arrival: Arrival, server: Server, independent=True, p=1.0):
        self.arrival = arrival
        self.server = server
        self.independent = independent
        self.p = p

    def sigma(self, theta: float) -> float:

        stability_check(self.arrival, self.server, theta, self.independent, self.p)
        sig_sum, rho_diff = sig_rho(self.arrival, self.server, theta, self.independent, self.p)

        if self.arrival.discrete():
            return sig_sum - (log(1 - exp(theta * rho_diff)) / theta)

        return self.arrival.rho(self.p*theta) + sig_sum - (log(1 - exp(theta * rho_diff)) / theta)

    def rho(self, theta: float) -> float:
        return self.arrival.rho(self.p*theta)

    def discrete(self) -> bool:
        return self.arrival.discrete()


class Convolve(Server):

    def __init__(self, server1: Server, server2: Server, independent=True, p=1.0):
        self.server1 = server1
        self.server2 = server2
        self.independent = independent
        self.p = p

        if independent:
            self.q = 1.0

        else:
            self.q = get_q(p)

    def sigma(self, theta: float) -> float:

        ser1_sigma = self.server1.sigma(self.p*theta)
        ser2_sigma = self.server2.sigma(self.q*theta)
        ser1_rho = self.server1.rho(self.p*theta)
        ser2_rho = self.server2.rho(self.q*theta)

        sigma_sum = ser1_sigma + ser2_sigma
        rho_diff = ser1_rho - ser2_rho

        if ser1_rho > ser2_rho:
            return sigma_sum - (log(1 - exp(theta * -rho_diff)) / theta)

        elif ser1_rho == ser2_rho:
            return sigma_sum

        return sigma_sum - (log(1 - exp(-theta * abs(-rho_diff))) / theta)

    def rho(self, theta: float) -> float:

        ser1_rho = self.server1.rho(self.p*theta)
        ser2_rho = self.server2.rho(self.q*theta)

        if ser1_rho > ser2_rho:
            return ser2_rho

        elif ser1_rho == ser2_rho:
            return ser1_rho - (1 / theta)

        return min(ser1_rho, ser2_rho)


class Leftovers(Server):

    def __init__(self, server: Server, cross_arrival: Arrival, independent=True, p=1.0):
        self.server = server
        self.cross_arrival = cross_arrival
        self.independent = independent
        self.p = p

    def sigma(self, theta: float) -> float:
        sig_sum, rho_diff = sig_rho(self.cross_arrival, self.server, theta, self.independent, self.p)

        return sig_sum

    def rho(self, theta: float) -> float:
        sig_sum, rho_diff = sig_rho(self.cross_arrival, self.server, theta, self.independent, self.p)

        return -rho_diff


class AggregateList(Arrival):

    def __init__(self, arrivals: List[Arrival], p_list: List[float], independent=True):
        self.arrivals = arrivals
        self.p_list = p_list
        self.independent = independent

        if len(self.p_list) != len(self.arrivals) - 1:
            raise ParameterOutOfBounds(f"Entries in the p_list should match num of arrivals-1")

        self.p_n = get_pn(self.p_list)

    def sigma(self, theta: float) -> float:

        result = 0.0
        if self.independent:
            for i in self.arrivals:
                result += i.sigma(theta)

            return result

        for i in range(len(self.arrivals) - 1):
            result += self.arrivals[i].sigma(self.p_list[i]*theta)

        result += self.arrivals[-1].sigma(self.p_n*theta)
        return result

    def rho(self, theta: float) -> float:

        result = 0.0
        if self.independent:
            for i in self.arrivals:
                result += i.rho(theta)

            return result

        for i in range(len(self.arrivals) - 1):
            rho_i = self.arrivals[i].rho(self.p_list[i] * theta)

            if rho_i < 0:
                raise ParameterOutOfBounds(f"Rhos must be >= 0")

            result += rho_i

        rho_n = self.arrivals[-1].rho(self.p_n * theta)

        if rho_n < 0:
            raise ParameterOutOfBounds(f"Rhos must be >= 0")

        result += rho_n

        return result

    def discrete(self) -> bool:
        return self.arrivals[0].discrete()


class AggregateHomogeneous(Arrival):

    def __init__(self, arrival: Arrival, n: int, independent=True):
        self.arrival = arrival
        self.n = n

        if not independent:
            raise NotImplementedError

    def sigma(self, theta: float) -> float:
        return self.n * self.arrival.sigma(theta)

    def rho(self, theta: float) -> float:
        return self.n * self.arrival.rho(theta)

    def discrete(self) -> bool:
        return self.arrival.discrete()
