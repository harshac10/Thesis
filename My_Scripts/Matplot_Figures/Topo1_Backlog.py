import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_excel('/root/Harsha/Result_Comparison/Result_Topo1.xlsx', sheet_name='Backlog')

backlog_prob = df['Backlog_Probability'].dropna(axis=0, how='any')

backlog_gd = df['Backlog'].loc[df['Optimization_Techniques'] == 'GRID_SEARCH']
backlog_nm = df['Backlog'].loc[df['Optimization_Techniques'] == 'NELDER-MEAD']
backlog_bh = df['Backlog'].loc[df['Optimization_Techniques'] == 'BASIN_HOPPING']
backlog_de = df['Backlog'].loc[df['Optimization_Techniques'] == 'DIFFERENTIAL_EVOLUTION']
backlog_da = df['Backlog'].loc[df['Optimization_Techniques'] == 'DUAL_ANNEALING']

plt.plot(backlog_prob,backlog_gd,marker='o',label='Grid_Search',linestyle='--')
plt.plot(backlog_prob,backlog_nm,marker='1',label='Nelder-Mead',linestyle='--')
plt.plot(backlog_prob,backlog_bh,marker='v',label='Basin_Hopping',linestyle='--')
plt.plot(backlog_prob,backlog_de,marker='<',label='Diff_Evolu',linestyle='--')
plt.plot(backlog_prob,backlog_da,marker='*',label='Dual_Ann',linestyle='--')

plt.xscale('log')

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title("Backlogs for Topology_1", fontsize=15)
plt.xlabel("Backlog_Probability", fontsize=15, labelpad=15)
plt.ylabel("Backlog_Value", fontsize=15, labelpad=15)
plt.legend()
plt.tight_layout()
plt.subplots_adjust(0.1,0.17,0.9,0.92)
plt.grid()
for i,j in zip(backlog_prob,backlog_gd):
    plt.annotate(str(j), xy=(i,j))
plt.show()