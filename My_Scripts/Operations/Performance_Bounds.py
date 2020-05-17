""" Evaluating Performance Bounds """

from Arrivals.Arrival import Arrival
from Servers.Server import Server
from Operations.Additional_Functions import get_q, sig_rho, stability_check
from math import exp, log, inf
import warnings


def backlog(arrival: Arrival, server: Server, theta: float, backlog_prob: float, independent=True, p=1.0,
            geo_series=True):

    if backlog_prob > 1.0 or backlog_prob < 0.0:
        raise ValueError(f"Probability value should be within (0,1)")

    if independent:
        q = 1.0
    else:
        q = get_q(p)

    stability_check(arrival, server, theta, independent, p)
    sig_sum, rho_diff = sig_rho(arrival, server, theta, independent, p)

    try:
        if geo_series:
            if arrival.discrete():
                log_part = log(1 - exp(theta * rho_diff)) + log(backlog_prob)
                return sig_sum - (log_part / theta)
            else:
                tau_opt = log(arrival.rho(p * theta) / server.rho(q * theta)) / (theta * rho_diff)
                log_part = log(backlog_prob * (1 - exp(theta * tau_opt * rho_diff))) / theta
                opt_res = arrival.rho(p * theta) * tau_opt + sig_sum - log_part / theta

                tau_1 = 1.0
                log_part = log(backlog_prob * (1 - exp(theta * tau_1 * rho_diff))) / theta
                one_res = arrival.rho(p * theta) * tau_1 + sig_sum - log_part / theta

                if one_res < opt_res:
                    warnings.warn("tau_opt yields worse result than tau_1")

                return min(opt_res, one_res)

        if arrival.discrete():
            log_part = log(-rho_diff * theta) + log(backlog_prob)
            return sig_sum - (log_part / theta)
        else:
            tau_opt = 1 / (theta * server.rho(q*theta))
            log_part = log(backlog_prob * (theta * tau_opt * -rho_diff)) / theta
            opt_res = server.rho(q*theta) * tau_opt + sig_sum - log_part

            tau_1 = 1.0
            log_part = log(backlog_prob * (theta * tau_1 * -rho_diff)) / theta
            one_res = server.rho(q * theta) * tau_1 + sig_sum - log_part

            if one_res < opt_res:
                warnings.warn("tau_opt yields worse result than tau_1")

            return min(opt_res, one_res)

    except ZeroDivisionError:
        return inf


def backlog_prob(arrival: Arrival, server: Server, theta: float, backlog_val: float, independent=True, p=1.0,
                 geo_series=True):

    if independent:
        q = 1.0
    else:
        q = get_q(p)

    stability_check(arrival, server, theta, independent, p)
    sig_sum, rho_diff = sig_rho(arrival, server, theta, independent, p)

    try:
        if geo_series:
            if arrival.discrete():
                return exp(-theta * backlog_val) * exp(theta * sig_sum) / (1 - exp(theta * rho_diff))
            else:
                tau_opt = log(arrival.rho(p * theta) / server.rho(q * theta)) / (theta * rho_diff)
                denom = 1 - exp(theta * tau_opt * rho_diff)
                opt_res = exp(-theta * backlog_val) * exp(theta * (arrival.rho(p * theta) * tau_opt + sig_sum)) / denom

                tau_1 = 1.0
                denom = 1 - exp(theta * tau_1 * rho_diff)
                one_res = exp(-theta * backlog_val) * exp(theta * (arrival.rho(p * theta) * tau_1 + sig_sum)) / denom

                if one_res < opt_res:
                    warnings.warn("tau_opt yields worse result than tau_1")

                return min(opt_res, one_res)

        if arrival.discrete():
            return exp(-theta * backlog_val) * exp(theta * sig_sum) / (-rho_diff * theta)
        else:
            tau_opt = 1 / (theta * server.rho(q * theta))
            denom = theta  * -rho_diff
            opt_res = exp(-theta * backlog_val) * exp(theta * (server.rho(q*theta) * tau_opt + sig_sum)) / denom

            tau_1 = 1.0
            one_res = exp(-theta * backlog_val) * exp(theta * (server.rho(q*theta) * tau_1 + sig_sum)) / denom

            if one_res < opt_res:
                warnings.warn("tau_opt yields worse result than tau_1")

            return min(opt_res, one_res)

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

    try:
        if geo_series:
            if arrival.discrete():
                log_part = log(delay_prob * (1 - exp(theta * rho_diff))) / theta
                result = (sig_sum - log_part) / server.rho(q * theta)
                return result
            else:
                tau_opt = log(arrival.rho(p * theta) / server.rho(q * theta)) / (theta * rho_diff)
                log_part = log(delay_prob * (1 - exp(theta * tau_opt * rho_diff))) / theta
                opt_res = (arrival.rho(p * theta) * tau_opt + sig_sum - log_part) / server.rho(q * theta)

                tau_1 = 1.0
                log_part = log(delay_prob * (1 - exp(theta * tau_1 * rho_diff))) / theta
                one_res = (arrival.rho(p * theta) * tau_1 + sig_sum - log_part) / server.rho(q * theta)

                if one_res < opt_res:
                    warnings.warn("tau_opt yields worse result than tau_1")

                return min(opt_res, one_res)

        if arrival.discrete():
            log_part = log(delay_prob * (-rho_diff * theta)) / theta
            return (sig_sum - log_part) / server.rho(q * theta)
        else:
            tau_opt = 1 / (theta * server.rho(q*theta))
            log_part = log(delay_prob * (theta * tau_opt * -rho_diff)) / theta
            opt_res = (server.rho(q*theta) * tau_opt + sig_sum - log_part) / server.rho(q * theta)

            tau_1 = 1.0
            log_part = log(delay_prob * (theta * tau_1 * -rho_diff)) / theta
            one_res = (server.rho(q * theta) * tau_1 + sig_sum - log_part) / server.rho(q * theta)

            if one_res < opt_res:
                warnings.warn("tau_opt yields worse result than tau_1")

            return min(opt_res, one_res)

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
                tau_opt = log(arrival.rho(p * theta) / server.rho(q * theta)) / (theta * rho_diff)
                denom = 1 - exp(theta * tau_opt * rho_diff)
                opt_res = exp(-theta * server.rho(q * theta) * delay_val) * \
                    exp(theta * (arrival.rho(p * theta) * tau_opt + sig_sum)) / denom

                tau_1 = 1.0
                denom = 1 - exp(theta * tau_1 * rho_diff)
                one_res = exp(-theta * server.rho(q * theta) * delay_val) * \
                          exp(theta * (arrival.rho(p * theta) * tau_1 + sig_sum)) / denom


                if one_res < opt_res:
                    warnings.warn("tau_opt yields worse result than tau_1")

                return min(opt_res, one_res)

        if arrival.discrete():
            return exp(-theta * server.rho(q * theta) * delay_val) * (exp(theta * sig_sum)) / (-rho_diff * theta)
        else:
            tau_opt = 1 / (theta * server.rho(q * theta))
            denom = theta * -rho_diff * tau_opt
            opt_res = exp(-theta * server.rho(q * theta) * delay_val) * \
                   exp(theta * (arrival.rho(p * theta) * tau_opt + sig_sum)) / denom

            tau_1 = 1.0
            denom = theta * -rho_diff * tau_1
            one_res = exp(-theta * server.rho(q * theta) * delay_val) * \
                      exp(theta * (arrival.rho(p * theta) * tau_1 + sig_sum)) / denom

            if one_res < opt_res:
                warnings.warn("tau_opt yields worse result than tau_1")

            return min(opt_res, one_res)

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
