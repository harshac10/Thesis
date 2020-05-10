""" Evaluating Performance Bounds """

from Arrivals.Arrival import Arrival
from Servers.Server import Server
from Performance_Bounds.Additional_Functions import get_q, sig_rho, stability_check
from math import exp, log, inf


def backlog(arrival: Arrival, server: Server, theta: float, backlog_prob: float, independent=True, p=1.0,
            geo_series=True):

    if backlog_prob > 1.0 or backlog_prob < 0.0:
        raise ValueError(f"Probability value should be within (0,1)")

    stability_check(arrival, server, theta, independent, p)
    sig_sum, rho_diff = sig_rho(arrival, server, theta, independent, p)
    tau = 1.0

    try:
        if geo_series:
            if arrival.discrete():
                log_part = log(1 - exp(theta * rho_diff)) + log(backlog_prob)
                return sig_sum - (log_part / theta)
            else:
                log_part = log(backlog_prob * (1 - exp(theta * tau * rho_diff))) / theta
                return arrival.rho(p * theta) * tau + sig_sum - log_part

        if arrival.discrete():
            log_part = log(-rho_diff * theta) + log(backlog_prob)
            return sig_sum - (log_part / theta)

        else:
            log_part = log(backlog_prob * (theta * tau * -rho_diff)) / theta
            return arrival.rho(p * theta) * tau + sig_sum - log_part

    except ZeroDivisionError:
        return inf


def backlog_prob(arrival: Arrival, server: Server, theta: float, backlog_val: float, independent=True, p=1.0,
                 geo_series=True):

    stability_check(arrival, server, theta, independent, p)
    sig_sum, rho_diff = sig_rho(arrival, server, theta, independent, p)
    tau = 1.0

    try:
        if geo_series:
            if arrival.discrete():
                return exp(-theta * backlog_val) * exp(theta * sig_sum) / (1 - exp(theta * rho_diff))

            else:
                denom = 1 - exp(theta * tau * rho_diff)
                return exp(-theta * backlog_val) * exp(theta * (arrival.rho(p * theta) + sig_sum)) / denom

        if arrival.discrete():
            return exp(-theta * backlog_val) * exp(theta * sig_sum) / (-rho_diff * theta)

        else:
            denom = theta * tau * -rho_diff
            return exp(-theta * backlog_val) * exp(theta * (arrival.rho(p * theta) + sig_sum)) / denom

    except ZeroDivisionError:
        return inf


def delay(arrival: Arrival, server: Server, theta: float, delay_prob: float, independent=True, p=1.0, geo_series=True):

    if delay_prob < 0.0 or delay_prob > 1.0:
        raise ValueError(f"Probability value should be in (0,1)")

    if independent:
        q = 1.0
    else:
        q = get_q(p)

    stability_check(arrival, server, theta, independent, p)
    sig_sum, rho_diff = sig_rho(arrival, server, theta, independent, p)
    tau = 1.0

    try:
        if geo_series:
            if arrival.discrete():
                log_part = log(delay_prob * (1 - exp(theta * rho_diff))) / theta
                result = (sig_sum - log_part) / server.rho(q * theta)
                return result
            else:
                log_part = log(delay_prob * (1 - exp(theta * tau * rho_diff))) / theta
                return (arrival.rho(p * theta) + sig_sum - log_part) / server.rho(q * theta)

        if arrival.discrete():
            log_part = log(delay_prob * (-rho_diff * theta)) / theta
            return (sig_sum - log_part) / server.rho(q * theta)
        else:
            log_part = log(delay_prob * (theta * tau * -rho_diff)) / theta
            return (arrival.rho(p * theta) + sig_sum - log_part) / server.rho(q * theta)

    except ZeroDivisionError:
        return inf


def delay_prob(arrival: Arrival, server: Server, theta: float, delay_val: float, independent=True, p=1.0,
               geo_series=True):

    if independent:
        q = 1.0
    else:
        q = get_q(p)

    stability_check(arrival, server, theta, independent, p)
    sig_sum, rho_diff = sig_rho(arrival, server, theta, independent, p)

    tau = 1.0

    try:
        if geo_series:
            if arrival.discrete():
                return exp(-theta * server.rho(q * theta) * delay_val) * \
                       (exp(theta * sig_sum)) / (1 - exp(theta * rho_diff))
            else:
                denom = 1 - exp(theta * tau * rho_diff)
                return exp(-theta * server.rho(q * theta) * delay_val) * \
                    exp(theta * (arrival.rho(p * theta) * tau + sig_sum)) / denom

        if arrival.discrete():
            return exp(-theta * server.rho(q * theta) * delay_val) * (exp(theta * sig_sum)) / (-rho_diff * theta)
        else:
            denom = theta * -rho_diff * tau
            return exp(-theta * server.rho(q * theta) * delay_val) * \
                   exp(theta * (arrival.rho(p * theta) * tau + sig_sum)) / denom

    except ZeroDivisionError:
        return inf


def output(arrival: Arrival, server: Server, theta: float, delta_time: int, independent=True, p=1.0):

    stability_check(arrival, server, theta, independent, p)
    sig_sum, rho_diff = sig_rho(arrival, server, theta, independent, p)

    try:
        if arrival.discrete():
            log_part = log(1 - exp(theta * rho_diff)) / theta
            return exp(theta * arrival.rho(p * theta) * delta_time) * exp(theta * (sig_sum - log_part))
        else:
            log_part = log(1 - exp(theta * rho_diff)) / theta
            return exp(theta * (arrival.rho(p * theta) * delta_time + arrival.rho(p * theta) + sig_sum - log_part))

    except ZeroDivisionError:
        return inf
