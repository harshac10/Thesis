#Computing Delay d(t)
import array as arr
import numpy as np
import math as m
#Generate theta
theta = np.linspace(0.1,10,10**6)
c = 0.9
eps = pow(10,-3)
print (theta,eps)
#Compute Qc and sigma
sig = arr.array('f')

for i in theta:
    Qc = m.exp(i*(1-c))/i
    print("Qc value is = "+ str(Qc))
    if (Qc < 1):
        sig.append(m.log(1/(eps*(1-Qc)))/i)

x = sorted(sig)
print("Sigma values are = ",x)
#d(t) = simga/c
delay = x[0]/c
print("Delay is = ",delay)