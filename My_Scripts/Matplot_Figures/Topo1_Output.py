import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_excel('/root/Harsha/Result_Comparison/Result_Topo1.xlsx', sheet_name='Output')

delta_time = df['Delta_Time'].dropna(axis=0, how='any')

output_gd = df['Output'].loc[df['Optimization_Techniques'] == 'GRID_SEARCH']
output_nm = df['Output'].loc[df['Optimization_Techniques'] == 'NELDER-MEAD']
output_bh = df['Output'].loc[df['Optimization_Techniques'] == 'BASIN_HOPPING']
output_de = df['Output'].loc[df['Optimization_Techniques'] == 'DIFFERENTIAL_EVOLUTION']
output_da = df['Output'].loc[df['Optimization_Techniques'] == 'DUAL_ANNEALING']

plt.plot(delta_time,output_gd,marker='o',label='Grid_Search',linestyle='--')
plt.plot(delta_time,output_nm,marker='1',label='Nelder-Mead',linestyle='--')
plt.plot(delta_time,output_bh,marker='v',label='Basin_Hopping',linestyle='--')
plt.plot(delta_time,output_de,marker='<',label='Diff_Evolu',linestyle='--')
plt.plot(delta_time,output_da,marker='*',label='Dual_Ann',linestyle='--')

plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.title("Output for Topology_1", fontsize=15)
plt.xlabel("Delta_Time", fontsize=15, labelpad=15)
plt.ylabel("Output_Value", fontsize=15, labelpad=15)
plt.legend()
plt.tight_layout()
plt.subplots_adjust(0.1,0.17,0.9,0.92)
plt.grid()
for i,j in zip(delta_time,output_gd):
    plt.annotate(str(j), xy=(i,j))
plt.show()
