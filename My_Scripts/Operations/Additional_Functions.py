""" Smaller but important functions """

from Arrivals.Arrival import Arrival
from Servers.Server import Server
from UD_Exceptions import ParameterOutOfBounds
from typing import List


def get_q(p: float) -> float:
    """ Hoelder´s inequality """

    if p <= 1.0:
        raise ParameterOutOfBounds(f"P value should be greater than 1")

    return p / (p - 1)


def get_pn(p_list: List[float]) -> float:

    """ p_list: p_1,p_2 etc and obtain last value i.e. p_n"""

    inv_p = [0.0] * len(p_list)

    for i, p_val in enumerate(p_list):

        if p_val <= 1.0:
            raise ParameterOutOfBounds(f"P value should be greater than 1")

        inv_p[i] = 1.0 / p_val

    return 1.0 / (1.0 - sum(inv_p))


def sig_rho(arrival: Arrival, server: Server, theta: float, independent: bool, p: float):

    if independent:
        return arrival.sigma(theta) + server.sigma(theta), arrival.rho(theta) - server.rho(theta)

    q = get_q(p)
    return arrival.sigma(p * theta) + server.sigma(q * theta), arrival.rho(p * theta) - server.rho(q * theta)


def stability_check(arrival: Arrival, server: Server, theta: float, independent: bool, p: float):

    if independent:

        if arrival.rho(theta) >= server.rho(theta):
            raise ParameterOutOfBounds(f"Stability condition is violated")

    else:
        q = get_q(p)

        if arrival.rho(p*theta) >= server.rho(q*theta):
            raise ParameterOutOfBounds(f"Server rho:{server.rho(q*theta)}, must be greater then "
                                       f"Arrival rho: {arrival.rho(p*theta)}")
