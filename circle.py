import numpy as np
import math

# Função para checar se o círculo contem o centro
def in_circle(center_x, center_y, radius, x_p, y_p):
    dist = math.sqrt((center_x - x_p) ** 2 + (center_y - y_p) ** 2)
    return dist <= radius

num_samples=10000
r1 = 1

# Cria um array de pontos aleatórios em um circulo com raio r1
rho = np.sqrt(np.random.uniform(0, r1, num_samples))
phi = np.random.uniform(0, 2*np.pi, num_samples)

x = rho * np.cos(phi)
y = rho * np.sin(phi)

t = 0
f = 0
# Para cada um dos pontos criados, cria um circulo com raio aleatório entre 0 e r1 e checa se esse circulo contem o centro de E1
for i in range(len(x)):    
    r2 = np.random.uniform(0, r1)
    if in_circle(x[i], y[i], r2, 0, 0):
        t += 1
    else:
        f += 1

print(t/num_samples)