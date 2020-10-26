#number = 112121212312123123213123121231212311199999999991231312312313112312134263463746276423424278348326482638462834672836482364273468237642783467822423654246526354263425425364563546256354256354265426346512312312312312313132325634563465376573645763745637465734665637457287827483248745838273847348572834784572948121321
from matplotlib import pyplot as plt
import numpy as np

arrImpares = []
arrPares = []
initNums = []
def calc(number):
    arr = []
    initNum = number
    initNums.append(initNum)
    arr.append(number)
    while number > 1:        
        if(number % 2) == 0:
            number = number/2
            arr.append(number)
        else:
            number = (number*3)+1
            arr.append(number)
    
    arrPares.append(len(arr))
    #if not ((initNum % 2) == 0):
    #    arrImpares.append(len(arr)) 
    #else:
    #    arrPares.append(len(arr))

for i in range(10000000):
    if (not (i == 0)) and (not (i == 1)):
        calc(i)

res = []
for i in range(len(arrPares)):
    res.append([initNums[i], arrPares[i]])

data = np.array(res)

x, y = data.T
plt.scatter(x,y,s=1)
plt.show()