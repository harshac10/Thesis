from Arrivals.Arrival import Arrival
from Servers.Server import Server
from Operations import Performance_Bounds
from Operations.Perform_Parameter import PerformParam, PerformEnum
from Operations.Network_Operations import AggregateHomogeneous


def evaluate_single_hop(foi: Arrival, s_e2e: Server, theta: float, perform_param: PerformParam,
                        independent=True, p=1.0, geo_series=True):

    if perform_param.perform_metric == PerformEnum.Backlog:
        return Performance_Bounds.backlog(foi, s_e2e, theta, perform_param.value, independent, p, geo_series)

    elif perform_param.perform_metric == PerformEnum.Backlog_Prob:
        return Performance_Bounds.backlog_prob(foi, s_e2e, theta, perform_param.value, independent, p, geo_series)

    elif perform_param.perform_metric == PerformEnum.Delay:
        return Performance_Bounds.delay(foi, s_e2e, theta, perform_param.value, independent, p, geo_series)

    elif perform_param.perform_metric == PerformEnum.Delay_Prob:
        return Performance_Bounds.delay_prob(foi, s_e2e, theta, perform_param.value, independent, p, geo_series)

    elif perform_param.perform_metric == PerformEnum.Output:
        return Performance_Bounds.output(foi, s_e2e, theta, perform_param.value, independent, p)

    else:
        raise NotImplementedError


def evaluate_homogeneous_aggregate(foi_single: Arrival, n: int, s_e2e: Server, theta: float,
                                   perform_param: PerformParam, independent=True, geo_series=True):

    if not independent:
        raise NotImplementedError

    if n > 1:
        return evaluate_single_hop(foi=AggregateHomogeneous(foi_single, n), s_e2e=s_e2e, theta=theta,
                                   perform_param=perform_param, geo_series=geo_series)

    else:
        evaluate_single_hop(foi=foi_single, s_e2e=s_e2e, theta=theta, perform_param=perform_param,
                            geo_series=geo_series)
