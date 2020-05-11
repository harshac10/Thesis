from Optimization.Setting import Setting
from Arrivals.Arrival_Distribution import ArrivalDistribution
from Arrivals.Queuing_Arrivals import DM1
from Arrivals.Basic_Arrivals import Poisson
from Servers.ConstantRate_Server import ConstantRateServer
from Servers.Server_Distribution import ServerDistribution
from Performance_Bounds.Perform_Parameter import PerformParam,PerformEnum
from Network_Operations.Network_Operations import Convolve, Leftovers
from Optimization.Evaluate_SingleHop import evaluate_single_hop
from Optimization.Optimization import Optimize
from typing import List
import csv
import pandas as pd


class Topology1(Setting):

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

        conv = Convolve(server1=s1, server2=s2)
        s_e2e = Leftovers(server=conv, cross_arrival=a2)
        with open('/root/Harsha/Result_Comparison/test.csv', mode='a+', newline='') as file_object:
            writer = csv.writer(file_object)
            writer.writerow([foi.rho(theta), s_e2e.rho(theta)])

        return evaluate_single_hop(foi=foi,s_e2e=s_e2e,theta=theta,perform_param=self.perform_param)

    def approx_util(self) -> float:
        pass


if __name__ == "__main__":
    delay_prob = PerformParam(PerformEnum.Delay,10**-5)
    foi = DM1(1.5)
    a2 = Poisson(0.5)
    ser1 = ConstantRateServer(2.0)
    ser2 = ConstantRateServer(2.5)

    with open('/root/Harsha/Result_Comparison/test.csv', mode='w', newline='') as file_object:
        writer = csv.writer(file_object)
        writer.writerow(["Arrival_Rho_Harsha","Server_Rho_Harsha"])

    with open('/root/Harsha/Result_Comparison/test.csv', mode='a+', newline='') as file_object:
        print(f"Delay = {Optimize(Topology1([foi, a2], [ser1, ser2], delay_prob), 1, False).grid_search([(0.5, 5.0)], 0.1)}",
              file=file_object)

    df = pd.read_csv("/root/Harsha/Result_Comparison/test.csv")
    df.to_excel("/root/Harsha/Result_Comparison/Result_Comparison1.xlsx", sheet_name="Delay_Topo1", index=False,
                header=True, startrow=0, startcol=0)

    print(f"Delay = {Optimize(Topology1([foi, a2], [ser1, ser2], delay_prob), 1, True).grid_search([(0.5, 5.0)], 0.1)}")