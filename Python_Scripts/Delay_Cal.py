from math import exp,inf,log
import numpy as np

def Qc_1(theta: float, c: float)-> float:
    return exp(theta*(1-c))/theta

def Qc_n(theta: float,c: float, flows: int)-> float:
    return (exp(theta*(1-c))/theta)**flows

def sigma_1(epsilon: float,theta: float, c:float)->float:
    if Qc_1(theta,c) >= 1:
        return inf
    theta_range.append(theta)
    return log(1/(epsilon* (1-Qc_1(theta,c))))/theta

def sigma(epsilon: float,theta: float, c:float)-> float:
    if Qc_n(theta,c,num_of_flows) >= 1:
        return inf
    theta_range.append(theta)
    return log(1 / (epsilon * (1 - Qc_n(theta,c,num_of_flows)))) / theta

sig = []
theta_range = []
theta = np.linspace(0.1,10,10**6,False)
per_rate = 0.75
eps = 10**-3
while(True):
    try:
        num_of_flows = int(input('Enter the number of flows:'))
        break
    except ValueError:
        print(f"The number must be an integer... Try again")

#Calculate delay for single flow
for i in theta:
     sig.append(sigma_1(epsilon=eps,theta=i,c=per_rate))

delay_1 = min(sig)/per_rate

#Calculate delay for multiplexing
if num_of_flows > 1:
    delay = 0
    for i in theta:
        sig.append(sigma(epsilon=eps, theta=i, c=per_rate))
    delay = min(sig) / per_rate
    print(f"The delay is: {delay} for c={per_rate}")
    while (delay <= delay_1 and per_rate > 0):
        sig.clear()
        theta_range.clear()
        per_rate -= 0.005
        for i in theta:
            sig.append(sigma(epsilon=eps,theta=i,c=per_rate))
        delay = min(sig)/per_rate
        print(f"The delay is: {delay} for c={per_rate}")
        if (delay < delay_1):
            delay_bound = delay
    per_rate += 0.005
    print(f"The final delay bound is: {delay_bound} for c = {per_rate}")
    print(f"The theta range if [{min(theta_range)},{max(theta_range)}]")
else:
    print(f"The theta range if [{min(theta_range)},{max(theta_range)}]")
    print(f"The delay is: {delay_1} for c={per_rate}")
