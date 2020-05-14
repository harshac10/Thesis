from Optimize.Setting import Setting
from Arrivals.Arrival_Distribution import ArrivalDistribution
from Arrivals.Queuing_Arrivals import DM1
from Arrivals.Basic_Arrivals import Poisson
from Servers.ConstantRate_Server import ConstantRateServer
from Servers.Server_Distribution import ServerDistribution
from Operations.Perform_Parameter import PerformParam,PerformEnum
from Operations.Network_Operations import Convolve, Leftovers
from Optimize.Evaluate_SingleHop import evaluate_single_hop
from Optimize.Optimization import Optimize
from typing import List
import numpy as np


class Topology2(Setting):

    def __init__(self, arr: List[ArrivalDistribution], ser: List[ServerDistribution], perform_param: PerformParam):
        self.arrival = arr
        self.server = ser
        self.perform_param = perform_param

    def standard_bound(self, param_list: List[float]) -> float:

        theta = param_list[0]
        foi = self.arrival[0]
        a2 = self.arrival[1]
        s1 = self.server[0]
        s2 = self.server[1]

        left_over = Leftovers(s2, a2)
        s_e2e = Convolve(s1, left_over)

        return evaluate_single_hop(foi=foi,s_e2e=s_e2e,theta=theta,perform_param=self.perform_param)

    def approx_util(self) -> float:
        pass


if __name__ == "__main__":

    delay = PerformParam(PerformEnum.Delay_Prob, 13.2)
    delay_prob = PerformParam(PerformEnum.Delay, 10 ** -5)
    backlog = PerformParam(PerformEnum.Backlog_Prob, 2.67)
    backlog_prob = PerformParam(PerformEnum.Backlog, 10 ** -6)
    delta_time = PerformParam(PerformEnum.Output, 2)

    foi = DM1(1.5)
    a2 = Poisson(0.5)
    ser1 = ConstantRateServer(2.0)
    ser2 = ConstantRateServer(2.5)
    initial_param = np.array([[0.1,5.0]])

    print(f"DUAL_ANNEALING")
    print(f"------------")

    delay_theta, delay_val = Optimize(Topology2([foi,a2],[ser1,ser2],delay_prob),1).dual_annealing([(0.5,7.2)])
    print(delay_theta,delay_val)
