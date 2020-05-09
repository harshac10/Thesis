""" Evaluating Performance Bounds """

from Arrivals.Arrival import Arrival
from Servers.Server import Server
from Operations_Performances.Additional_Functions import get_q, sig_rho, stability_check
from math import exp, log


def backlog(arrival: Arrival, server: Server, theta: float, backlog_prob: float, independent=True, p=1.0, geo_series=True):

    if backlog_prob > 1.0 or backlog_prob < 0.0:
        raise ValueError(f"Probability value should be within (0,1)")

    if stability_check(arrival, server, theta):
        sig_sum, rho_diff = sig_rho(arrival, server, theta, independent, p)
        tau = 1.0

        if geo_series:

            if arrival.discrete():
                log_part = log(1 - exp(theta * rho_diff)) + log(backlog_prob)
                return sig_sum - (log_part / theta)

            log_part = log(backlog_prob * (1 - exp(theta * tau * rho_diff))) / theta
            return arrival.rho(p*theta) * tau + sig_sum - log_part

        if arrival.discrete():
            log_part = log(-rho_diff * theta) + log(backlog_prob)
            return sig_sum - (log_part / theta)

        log_part = log(backlog_prob * (theta * tau * -rho_diff)) / theta
        return arrival.rho(p * theta) * tau + sig_sum - log_part

    raise ValueError(f"Stability condition is violated")


def backlog_prob(arrival: Arrival, server: Server, theta: float, backlog_val: float, independent=True, p=1.0, geo_series=True):

    if stability_check(arrival, server, theta):
        sig_sum , rho_diff = sig_rho(arrival, server,theta, independent, p)
        tau = 1.0

        if geo_series:
            if arrival.discrete():
                return exp(-theta * backlog_val) * exp(theta * sig_sum) / (1 - exp(theta * rho_diff))

            denom = 1 - exp(theta * tau * rho_diff)
            return exp(-theta * backlog_val) * exp(theta * (arrival.rho(p*theta) + sig_sum)) / denom

        if arrival.discrete():
            return exp(-theta * backlog_val) * exp(theta * sig_sum) / (-rho_diff * theta)

        denom = theta * tau * -rho_diff
        return exp(-theta * backlog_val) * exp(theta * (arrival.rho(p * theta) + sig_sum)) / denom

    raise ValueError(f"Stability condition violated")


def delay(arrival: Arrival, server: Server, theta: float, delay_prob: float, independent=True, p=1.0, geo_series=True):

    if delay_prob < 0.0 or delay_prob > 1.0:
        raise ValueError(f"Probability value should be in (0,1)")

    if stability_check(arrival, server, theta):
        q = get_q(p)
        sig_sum, rho_diff = sig_rho(arrival, server, theta, independent, p)
        tau = 1.0

        if geo_series:
            if arrival.discrete():
                log_part = log(delay_prob * (1 - exp(theta * rho_diff))) / theta
                return (sig_sum - log_part) / server.rho(q * theta)

            log_part = log(delay_prob * (1 - exp(theta * tau * rho_diff))) / theta
            return (arrival.rho(p*theta) + sig_sum - log_part) / server.rho(q*theta)

        if arrival.discrete():
            log_part = log(delay_prob * (-rho_diff * theta)) / theta
            return (sig_sum - log_part) / server.rho(q * theta)

        log_part = log(delay_prob * (theta * tau * -rho_diff)) / theta
        return (arrival.rho(p*theta) + sig_sum - log_part) / server.rho(q*theta)

    raise ValueError(f"Stability condition is violated")


def delay_prob(arrival: Arrival, server: Server, theta: float, delay_val: float, independent=True, p=1.0, geo_series=True):

    if stability_check(arrival, server, theta):
        sig_sum, rho_diff = sig_rho(arrival, server, theta, independent, p)
        q = get_q(p)
        tau = 1.0

        if geo_series:
            if arrival.discrete():
                return exp(-theta * server.rho(q * theta) * delay_val) *\
                       (exp(theta * sig_sum)) / (1 - exp(theta * rho_diff))

            denom = 1 - exp(theta * tau * rho_diff)
            return exp(-theta * server.rho(q*theta) * delay_val) *\
                   exp(theta * (arrival.rho(p*theta) * tau + sig_sum)) / denom

        if arrival.discrete():
            return exp(-theta * server.rho(q * theta) * delay_val) * (exp(theta * sig_sum)) / (-rho_diff * theta)

        denom = theta * -rho_diff * tau
        return exp(-theta * server.rho(q*theta) * delay_val) *\
                exp(theta * (arrival.rho(p*theta) * tau + sig_sum)) / denom

    raise ValueError(f"Stability condition is violated")


def output(arrival: Arrival, server: Server, theta: float, delta_time: int, independent=True, p=1.0):

    if stability_check(arrival, server, theta):
        sig_sum, rho_diff = sig_rho(arrival, server, theta, independent, p)

        if arrival.discrete():
            log_part = log(1 - exp(theta * rho_diff)) / theta
            return exp(theta * arrival.rho(p*theta) * delta_time) * exp(theta * (sig_sum - log_part))

        log_part = log(1 - exp(theta * rho_diff)) / theta
        return exp(theta * (arrival.rho(p*theta) * delta_time + arrival.rho(p*theta) + sig_sum - log_part))

    raise ValueError(f"Stability condition violated")
