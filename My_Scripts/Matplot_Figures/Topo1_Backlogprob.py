import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_excel('/root/Harsha/Result_Comparison/Result_Topo1.xlsx', sheet_name='Backlog_Prob')

backlog_value = df['Backlog'].dropna(axis=0, how='any')

backlog_prob_gd = df['Backlog_Probability'].loc[df['Optimization_Techniques'] == 'GRID_SEARCH']
backlog_prob_nm = df['Backlog_Probability'].loc[df['Optimization_Techniques'] == 'NELDER-MEAD']
backlog_prob_bh = df['Backlog_Probability'].loc[df['Optimization_Techniques'] == 'BASIN_HOPPING']
backlog_prob_de = df['Backlog_Probability'].loc[df['Optimization_Techniques'] == 'DIFFERENTIAL_EVOLUTION']
backlog_prob_da = df['Backlog_Probability'].loc[df['Optimization_Techniques'] == 'DUAL_ANNEALING']

plt.plot(backlog_value,backlog_prob_gd,marker='o',label='Grid_Search',linestyle='--')
plt.plot(backlog_value,backlog_prob_nm,marker='1',label='Nelder-Mead',linestyle='--')
plt.plot(backlog_value,backlog_prob_bh,marker='v',label='Basin_Hopping',linestyle='--')
plt.plot(backlog_value,backlog_prob_de,marker='<',label='Diff_Evolu',linestyle='--')
plt.plot(backlog_value,backlog_prob_da,marker='*',label='Dual_Ann',linestyle='--')

plt.yscale('log')

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title("Backlog_Probabilities for Topology_1", fontsize=15)
plt.xlabel("Backlog_Value", fontsize=15, labelpad=15)
plt.ylabel("Backlog_Probability", fontsize=15, labelpad=15)
plt.legend()
plt.tight_layout()
plt.subplots_adjust(0.1,0.17,0.9,0.92)
plt.grid()
for i,j in zip(backlog_value,backlog_prob_gd):
    plt.annotate(str(j), xy=(i,j))
plt.show()