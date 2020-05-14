from Optimize.Setting import Setting
from Arrivals.Arrival_Distribution import ArrivalDistribution
from Arrivals.Queuing_Arrivals import MM1
from Arrivals.Markov_Models import MarkovModelCont, MarkovModelDisc
from Servers.Server_Distribution import ServerDistribution
from Servers.ConstantRate_Server import ConstantRateServer
from Operations.Perform_Parameter import PerformParam, PerformEnum
from Operations.Network_Operations import Convolve, Leftovers
from Optimize.Evaluate_SingleHop import evaluate_single_hop
from Optimize.Optimization import Optimize
from typing import List
import pandas as pd
import csv


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

    delay = PerformParam(PerformEnum.Delay_Prob, 6.2)
    delay_prob = PerformParam(PerformEnum.Delay, 10 ** -2)
    backlog = PerformParam(PerformEnum.Backlog_Prob, 1.45)
    backlog_prob = PerformParam(PerformEnum.Backlog, 10**-8)
    output = PerformParam(PerformEnum.Output, 1)

    foi = MM1(1.5, 0.69)
    a2 = MarkovModelDisc(0.98, 0.15, 0.01)
    a3 = MarkovModelCont(2.8, 0.56, 0.08)
    s1 = ConstantRateServer(5.8)
    s2 = ConstantRateServer(3.58)
    s3 = ConstantRateServer(4.8)

    print(f"GRID SEARCH")
    print(f"------------")

    delay_theta, delay_val = Optimize(Topology3([foi,a2,a3], [s1,s2],delay_prob),1).grid_search([(0.1,6.0)],0.1)
    dprob_theta, dprob_val = Optimize(Topology3([foi, a2, a3], [s1, s2], delay), 1).grid_search([(0.1, 6.0)], 0.1)
    backlog_theta, backlog_val = Optimize(Topology3([foi, a2, a3], [s1, s2], backlog_prob), 1).grid_search([(0.1, 6.0)], 0.1)
    bprob_theta, bprob_val = Optimize(Topology3([foi, a2, a3], [s1, s2], backlog), 1).grid_search([(0.1, 6.0)], 0.1)
    output_theta, output_val = Optimize(Topology3([foi, a2, a3], [s1, s2], output), 1).grid_search([(0.1, 6.0)], 0.1)

    with open("/root/Harsha/Result_Comparison/Result.csv", mode='a+', newline='') as performfile:
        writer = csv.writer(performfile)
        writer.writerow(["Performance_Bounds", "Optimal X", "Value"])
        writer.writerow(["Delay", delay_theta, delay_val])
        writer.writerow(["Delay_Probability", dprob_theta, dprob_val])
        writer.writerow(["Backlog", backlog_theta, backlog_val])
        writer.writerow(["Backlog_Probability", bprob_theta, bprob_val])
        writer.writerow(["Output", output_theta, output_val])

    df = pd.read_csv("/root/Harsha/Result_Comparison/Result.csv", skiprows= 12)
    print(df)
