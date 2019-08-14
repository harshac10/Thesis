#Computing delay bound, given the probability, for single and multiple flows
import numpy as np
import math
theta = np.linspace(0.1,10,10**6)
c = 0.75 #per flow rate
eps = pow(10,-3) #probablity
sig = []
theta_range = []
while(True):
    try:
        Num_flows = int(input("Enter the number of flows in integer: "))
        break
    except ValueError:
        print(f"Sorry the number is not an integer... Try again")

#Calculate delay for single flow
for i in theta:
    Qc_1 = (math.exp(i*(1-c))/i)
    if Qc_1 < 1:
        sig.append(math.log(1/(eps * (1-Qc_1)))/i)
        theta_range.append(i)

delay_1 = min(sig)/c

if int(Num_flows) > 1:
    delay = 0
    while delay <= delay_1 and c > 0:
        sig.clear()
        theta_range.clear()
        for j in theta:
            Qc = (math.exp(j * (1 - c)) / j) ** int(Num_flows)
            if Qc < 1:
                sig.append(math.log(1 / (eps * (1 - Qc))) / j)
                theta_range.append(j)
        delay = min(sig)/c
        c = c - 0.005
    print(f"The range of theta is [{min(theta_range)} , {max(theta_range)}]")
    print(f"The delay bound is: {delay} for c = {c}")
else:
    print(f"The range of theta is [{min(theta_range)} , {max(theta_range)}]")
    print(f"The delay bound is: {delay_1} for c = {c}")





















