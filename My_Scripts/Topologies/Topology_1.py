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
import pandas as pd
import numpy as np
import csv
import os


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

        return evaluate_single_hop(foi=foi,s_e2e=s_e2e,theta=theta,perform_param=self.perform_param)

    def approx_util(self) -> float:
        pass


if __name__ == "__main__":

    delay_value = 10.0
    prob_value = 1
    backlog_value = 0.0

    delay = PerformParam(PerformEnum.Delay_Prob, delay_value)
    delay_prob = PerformParam(PerformEnum.Delay, 10**(-prob_value))
    backlog = PerformParam(PerformEnum.Backlog_Prob, backlog_value)
    backlog_prob = PerformParam(PerformEnum.Backlog, 10**(-prob_value))
    delta_time = PerformParam(PerformEnum.Output, prob_value)

    theta = 0.1, 5.0

    foi = DM1(1.5)
    a2 = Poisson(0.5)
    ser1 = ConstantRateServer(2.0)
    ser2 = ConstantRateServer(2.5)

    """
    Calculating Delay Probabilities
    """
    os.remove("/root/Harsha/Result_Comparison/Result.csv")
    with open("/root/Harsha/Result_Comparison/Result.csv", mode='a+', newline='') as performfile:
        writer = csv.writer(performfile)
        writer.writerow([ "Delay","Optimization_Techniques", "Delay_Probability", "Optimal_X"])
        i = 0

        while i < 5:

            dprob_theta, dprob_val = Optimize(Topology1([foi, a2], [ser1, ser2], delay), 1).grid_search([theta], 0.1)
            dprob_theta_nm, dprob_val_nm = Optimize(Topology1([foi,a2],[ser1,ser2],delay),1).nelder_mead(np.array([theta]))
            dprob_theta_bh, dprob_val_bh = Optimize(Topology1([foi, a2], [ser1, ser2], delay), 1).basin_hopping([0.1,5.0])
            dprob_theta_de, dprob_val_de = Optimize(Topology1([foi, a2], [ser1, ser2], delay), 1).diff_evolution([theta])
            dprob_theta_da, dprob_val_da = Optimize(Topology1([foi, a2], [ser1, ser2], delay), 1).dual_annealing([theta])

            writer.writerow([delay.value,"GRID_SEARCH", dprob_val, dprob_theta])
            writer.writerow(['',"NELDER-MEAD", dprob_val_nm, dprob_theta_nm])
            writer.writerow(['',"BASIN_HOPPING", dprob_val_bh, dprob_theta_bh])
            writer.writerow(['',"DIFFERENTIAL_EVOLUTION", dprob_val_de, dprob_theta_de])
            writer.writerow(['',"DUAL_ANNEALING", dprob_val_da, dprob_theta_da])

            delay_value += 5.0
            delay = PerformParam(PerformEnum.Delay_Prob, delay_value)
            i += 1

    df = pd.read_csv("/root/Harsha/Result_Comparison/Result.csv")

    """
    Calculating Backlog_Probabilities
    """
    os.remove("/root/Harsha/Result_Comparison/Result.csv")
    with open("/root/Harsha/Result_Comparison/Result.csv", mode='a+', newline='') as performfile:
        writer = csv.writer(performfile)
        writer.writerow(["Backlog","Optimization_Techniques", "Backlog_Probability", "Optimal_X"])
        i = 0

        while i < 5:

            bprob_theta, bprob_val = Optimize(Topology1([foi, a2], [ser1, ser2], backlog), 1).grid_search([theta], 0.1)
            bprob_theta_nm, bprob_val_nm = Optimize(Topology1([foi,a2],[ser1,ser2],backlog),1).nelder_mead(np.array([theta]))
            bprob_theta_bh, bprob_val_bh = Optimize(Topology1([foi, a2], [ser1, ser2], backlog), 1).basin_hopping([0.1,5.0])
            bprob_theta_de, bprob_val_de = Optimize(Topology1([foi, a2], [ser1, ser2], backlog), 1).diff_evolution([theta])
            bprob_theta_da, bprob_val_da = Optimize(Topology1([foi, a2], [ser1, ser2], backlog), 1).dual_annealing([theta])

            writer.writerow([backlog.value,"GRID_SEARCH", bprob_val, bprob_theta])
            writer.writerow(['',"NELDER-MEAD", bprob_val_nm, bprob_theta_nm])
            writer.writerow(['',"BASIN_HOPPING", bprob_val_bh, bprob_theta_bh])
            writer.writerow(['',"DIFFERENTIAL_EVOLUTION", bprob_val_de, bprob_theta_de])
            writer.writerow(['',"DUAL_ANNEALING", bprob_val_da, bprob_theta_da])

            backlog_value += 2.0
            backlog = PerformParam(PerformEnum.Backlog_Prob, backlog_value)
            i += 1

    df1 = pd.read_csv("/root/Harsha/Result_Comparison/Result.csv")

    """
    Calculating Delays
    """
    os.remove("/root/Harsha/Result_Comparison/Result.csv")
    with open("/root/Harsha/Result_Comparison/Result.csv", mode='a+', newline='') as performfile:
        writer = csv.writer(performfile)
        writer.writerow(["Delay_Probability", "Optimization_Techniques", "Delay", "Optimal_X"])
        i = 0

        while i < 5:
            delay_theta, delay_val = Optimize(Topology1([foi, a2], [ser1, ser2], delay_prob), 1).grid_search([theta], 0.1)
            delay_theta_nm, delay_val_nm = Optimize(Topology1([foi,a2],[ser1,ser2],delay_prob),1).nelder_mead(np.array([theta]))
            delay_theta_bh, delay_val_bh = Optimize(Topology1([foi, a2], [ser1, ser2], delay_prob), 1).basin_hopping([0.1,5.0])
            delay_theta_de, delay_val_de = Optimize(Topology1([foi, a2], [ser1, ser2], delay_prob), 1).diff_evolution([theta])
            delay_theta_da, delay_val_da = Optimize(Topology1([foi, a2], [ser1, ser2], delay_prob), 1).dual_annealing([theta])

            writer.writerow([delay_prob.value, "GRID_SEARCH", delay_val, delay_theta])
            writer.writerow(['', "NELDER-MEAD", delay_val_nm, delay_theta_nm])
            writer.writerow(['', "BASIN_HOPPING", delay_val_bh, delay_theta_bh])
            writer.writerow(['', "DIFFERENTIAL_EVOLUTION", delay_val_de, delay_theta_de])
            writer.writerow(['', "DUAL_ANNEALING", delay_val_da, delay_theta_da ])

            prob_value += 2.0
            delay_prob = PerformParam(PerformEnum.Delay, 10**(-prob_value))
            i += 1

    df2 = pd.read_csv("/root/Harsha/Result_Comparison/Result.csv")

    """
    Calculating Backlogs
    """
    os.remove("/root/Harsha/Result_Comparison/Result.csv")
    with open("/root/Harsha/Result_Comparison/Result.csv", mode='a+', newline='') as performfile:
        writer = csv.writer(performfile)
        writer.writerow(["Backlog_Probability", "Optimization_Techniques", "Backlog", "Optimal_X"])
        i = 0
        prob_value = 1

        while i < 5:
            backlog_theta, backlog_val = Optimize(Topology1([foi, a2], [ser1, ser2], backlog_prob), 1).grid_search([theta], 0.1)
            backlog_theta_nm, backlog_val_nm = Optimize(Topology1([foi,a2],[ser1,ser2],backlog_prob),1).nelder_mead(np.array([theta]))
            backlog_theta_bh, backlog_val_bh = Optimize(Topology1([foi, a2], [ser1, ser2], backlog_prob), 1).basin_hopping([0.1,5.0])
            backlog_theta_de, backlog_val_de = Optimize(Topology1([foi, a2], [ser1, ser2], backlog_prob), 1).diff_evolution([theta])
            backlog_theta_da, backlog_val_da = Optimize(Topology1([foi, a2], [ser1, ser2], backlog_prob), 1).dual_annealing([theta])

            writer.writerow([backlog_prob.value, "GRID_SEARCH", backlog_val, backlog_theta])
            writer.writerow(['', "NELDER-MEAD", backlog_val_nm, backlog_theta_nm])
            writer.writerow(['', "BASIN_HOPPING", backlog_val_bh, backlog_theta_bh])
            writer.writerow(['', "DIFFERENTIAL_EVOLUTION", backlog_val_de, backlog_theta_de])
            writer.writerow(['', "DUAL_ANNEALING", backlog_val_da, backlog_theta_da])

            prob_value += 2.0
            backlog_prob = PerformParam(PerformEnum.Backlog, 10**(-prob_value))
            i += 1

    df3 = pd.read_csv("/root/Harsha/Result_Comparison/Result.csv")

    """
    Calculating Outputs
    """
    os.remove("/root/Harsha/Result_Comparison/Result.csv")
    with open("/root/Harsha/Result_Comparison/Result.csv", mode='a+', newline='') as performfile:
        writer = csv.writer(performfile)
        writer.writerow(["Delta_Time", "Optimization_Techniques", "Output", "Optimal_X"])
        i = 0
        prob_value = 1

        while i < 5:

            output_theta, output_val = Optimize(Topology1([foi, a2], [ser1, ser2], delta_time), 1).grid_search([theta], 0.1)
            output_theta_nm, output_val_nm = Optimize(Topology1([foi,a2],[ser1,ser2],delta_time),1).nelder_mead(np.array([theta]))
            output_theta_bh, output_val_bh = Optimize(Topology1([foi, a2], [ser1, ser2], delta_time), 1).basin_hopping([0.1,5.0])
            output_theta_de, output_val_de = Optimize(Topology1([foi, a2], [ser1, ser2], delta_time), 1).diff_evolution([theta])
            output_theta_da, output_val_da = Optimize(Topology1([foi, a2], [ser1, ser2], delta_time), 1).dual_annealing([theta])

            writer.writerow([delta_time.value, "GRID_SEARCH", output_val, output_theta])
            writer.writerow(['', "NELDER-MEAD", output_val_nm, output_theta_nm])
            writer.writerow(['', "BASIN_HOPPING", output_val_bh, output_theta_bh])
            writer.writerow(['', "DIFFERENTIAL_EVOLUTION", output_val_de, output_theta_de])
            writer.writerow(['', "DUAL_ANNEALING", output_val_da, output_theta_da])

            prob_value += 1
            delta_time = PerformParam(PerformEnum.Output, prob_value)
            i += 1

    df4 = pd.read_csv("/root/Harsha/Result_Comparison/Result.csv")

    ex_writer = pd.ExcelWriter('/root/Harsha/Result_Comparison/Result_Topo1.xlsx')
    df.to_excel(ex_writer, sheet_name='Delay_Prob', index=False)
    df1.to_excel(ex_writer, sheet_name='Backlog_Prob', index=False)
    df2.to_excel(ex_writer, sheet_name='Delay', index=False)
    df3.to_excel(ex_writer, sheet_name='Backlog', index=False)
    df4.to_excel(ex_writer, sheet_name='Output', index=False)
    ex_writer.save()
