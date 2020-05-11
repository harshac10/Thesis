from Optimization.Setting import Setting
from Arrivals.Arrival_Distribution import ArrivalDistribution
from Arrivals.Queuing_Arrivals import MM1
from Arrivals.Markov_Models import MarkovModelCont, MarkovModelDisc
from Servers.Server_Distribution import ServerDistribution
from Servers.ConstantRate_Server import ConstantRateServer
from Performance_Bounds.Perform_Parameter import PerformParam, PerformEnum
from Network_Operations.Network_Operations import Convolve, Leftovers
from Optimization.Evaluate_SingleHop import evaluate_single_hop
from Optimization.Optimization import Optimize
from typing import List


class Topology3(Setting):

    def __init__(self, arrivals: List[ArrivalDistribution], servers: List[ServerDistribution],
                 perform_parameter: PerformParam):
        self.arrivals = arrivals
        self.servers = servers
        self.perform_param = perform_parameter

    def standard_bound(self, param_list: List[float]) -> float:
        theta = param_list[0]
        a_foi = self.arrivals[0]
        a2 = self.arrivals[1]
        a3 = self.arrivals[2]
        ser1 = self.servers[0]
        ser2 = self.servers[1]

        left_over = Leftovers(ser2, a3)
        conv = Convolve(ser1, left_over)
        s_e2e = Leftovers(conv, a2)

        return evaluate_single_hop(a_foi, s_e2e, theta, self.perform_param)

    def approx_util(self) -> float:
        pass


if __name__ == "__main__":

    backlog_prob = PerformParam(PerformEnum.Backlog, 10**-3)
    foi = MM1(1.5, 0.69)
    a2 = MarkovModelDisc(1.0, 0.0, 0.01)
    a3 = MarkovModelCont(2.8, 0.56, 0.08)
    s1 = ConstantRateServer(5.8, 0.0)
    s2 = ConstantRateServer(3.58, 0.0)
    s3 = ConstantRateServer(4.8, 0.0)

    print(f"Backlog = {Optimize(Topology3([foi,a2,a3], [s1,s2],backlog_prob),1).grid_search([(0.1,6.0)],0.1)}")

