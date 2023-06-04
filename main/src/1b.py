from lib1 import RK4, scale_plot
import numpy as np

#parametros:

M = 1783 #Kg, massa do carro
k1 = k2 = 2.8e7 #N/m, cte das molas das suspensoes
c1 = c2 = 3e4 #Kg/s, cte de amortecimento suspensoes
a = 1220e-3 #m, distancia entre pto de apoio suspensao dianteira
b = 1500e-3 #m, distancia entre pto de apoio suspensao traseira
Ic = 4000 #kg.m^2, mom. de inercia do carro
e = 0.75 #m, distancia entre c.m. eixo do carro e cm do motor
L = 0.5 #m, comprimento da oscilacao do solo
A = 60e-3 #m, amplitude da oscilacao do solo
f = 0.35 #m, dist em y entre o centro do eixo do carro e o eixo do motor
vel = 50/3.6 #m/s, velocidade do carro
re = 0.045 #m, raio de giro do virabrequim
me = 20 #kg, massa do virabrequim
fe = 2100/60 #rpm, frequencia de rot. do virabrequim

omegae = fe*2*np.pi

Fn = me*(omegae**2)*re

omega = 2*np.pi*vel/L


def d1(A, omega, t):
    if t < 2:
        return A*(1-np.cos(omega*t))
    else:
        return 0

def d1p (A, omega, t):
    if t < 2:
        return A*omega*np.sin(omega*t)
    else:
        return 0
    
def d2(A, omega, t):
    if t < 2:
        return A*(1+np.cos(omega*t))
    else:
        return 0

def d2p (A, omega, t):
    if t < 2:
        return -A*omega*np.sin(omega*t)
    else:
        return 0
    

#instante inicial:
t_0 = 0
theta_0 = 0.09 #rad, inclinacao inicial do carro
x_0 = 0
xp_0 = 0
thetap_0 = 0

t = t_0
x = x_0
xp = xp_0
theta = theta_0
thetap = thetap_0


Y0 = [x, xp, theta, thetap]



#
# F = [
#    xp,
#    (-k1*(x-a*theta-d1(A, omega, t))-k2*(x+b*theta-d2(A, omega, t))-c1*(xp-a*thetap-d1p(A,omega,t))-c2*(xp+b*thetap-d2p(A,omega,t))+Fn*np.sin(omegae*t))/M,
#    thetap,
#    (k1*(x-a*theta-d1(A, omega,t))*a-k2*(x+b*theta-d2(A,omega,t))*b+c1*(xp-a*thetap-d1p(A,omega,t))*a-c2*(xp+b*thetap-d2p(A,omega,t))*b-Fn*np.sin(omegae*t)-Fn*np.cos(omegae*t)*f)/Ic]


steps = [1e-4]

# letra 1.b.i
for variacao in [30/3.6, 70/3.6]:
    vel = variacao
    omega = 2*np.pi*vel/L
    f1 = lambda t, Y: (Y[1])
    f2 = lambda t, Y: ((-k1*(Y[0]-a*Y[2]-d1(A, omega, t))-k2*(Y[0]+b*Y[2]-d2(A, omega, t))-c1*(Y[1]-a*Y[3]-d1p(A,omega,t))-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))+Fn*np.sin(omegae*t))/M)
    f3 = lambda t, Y: Y[3]
    f4 = lambda t, Y: (k1*(Y[0]-a*Y[2]-d1(A, omega,t))*a-k2*(Y[0]+b*Y[2]-d2(A,omega,t))*b+c1*(Y[1]-a*Y[3]-d1p(A,omega,t))*a-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))*b-Fn*np.sin(omegae*t)-Fn*np.cos(omegae*t)*f)/Ic
    F = [f1, f2, f3, f4]
    for h in steps:
        T, Y_hist, K1_hist = RK4(F, t_0, Y0, h, tf=4)

        Y = np.vstack([Y_hist[0:2], K1_hist[1], Y_hist[2:], K1_hist[3]])

        scale_plot(
            T, Y,
            title  = f"RK4 com passo h = {h} e velocidade V = {round(vel*3.6)} km/h",
            ylabel = "$x, \\dot{x}, \\ddot{x}, \\theta, \\dot{\\theta}, \\ddot{\\theta}$ (SI × 10^x)",
            xlabel = "Tempo (s)",
            legend = ['x', 'xp', 'xpp', 'theta', 'thetap', 'thetapp']
            #legend = ['x', 'xp', 'theta', 'thetap', 'xpp', 'thetapp']
        )

vel = 50/3.6 #retorna pro valor normal
omega = 2*np.pi*vel/L


#parte 1.b.ii

for variacao in [1e3, 5e4, 2.5e5]:
    c1 = c2 = variacao
    f1 = lambda t, Y: (Y[1])
    f2 = lambda t, Y: ((-k1*(Y[0]-a*Y[2]-d1(A, omega, t))-k2*(Y[0]+b*Y[2]-d2(A, omega, t))-c1*(Y[1]-a*Y[3]-d1p(A,omega,t))-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))+Fn*np.sin(omegae*t))/M)
    f3 = lambda t, Y: Y[3]
    f4 = lambda t, Y: (k1*(Y[0]-a*Y[2]-d1(A, omega,t))*a-k2*(Y[0]+b*Y[2]-d2(A,omega,t))*b+c1*(Y[1]-a*Y[3]-d1p(A,omega,t))*a-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))*b-Fn*np.sin(omegae*t)-Fn*np.cos(omegae*t)*f)/Ic
    F = [f1, f2, f3, f4]
    for h in steps:
        T, Y_hist, K1_hist = RK4(F, t_0, Y0, h, tf=4)

        Y = np.vstack([Y_hist[0:2], K1_hist[1], Y_hist[2:], K1_hist[3]])

        scale_plot(
            T, Y,
            title  = f"RK4 com passo h = {h} e c1 = c2 = {c1} kg/s",
            ylabel = "$x, \\dot{x}, \\ddot{x}, \\theta, \\dot{\\theta}, \\ddot{\\theta}$ (SI × 10^x)",
            xlabel = "Tempo (s)",
            legend = ['x', 'xp', 'xpp', 'theta', 'thetap', 'thetapp']
            #legend = ['x', 'xp', 'theta', 'thetap', 'xpp', 'thetapp']
        )

c1 = c2 = 3e4 #volta pro valor normal


#parte 1.b.iii

for variacao in [2e4, 5e6, 7e8]:
    k1 = k2 = variacao
    f1 = lambda t, Y: (Y[1])
    f2 = lambda t, Y: ((-k1*(Y[0]-a*Y[2]-d1(A, omega, t))-k2*(Y[0]+b*Y[2]-d2(A, omega, t))-c1*(Y[1]-a*Y[3]-d1p(A,omega,t))-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))+Fn*np.sin(omegae*t))/M)
    f3 = lambda t, Y: Y[3]
    f4 = lambda t, Y: (k1*(Y[0]-a*Y[2]-d1(A, omega,t))*a-k2*(Y[0]+b*Y[2]-d2(A,omega,t))*b+c1*(Y[1]-a*Y[3]-d1p(A,omega,t))*a-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))*b-Fn*np.sin(omegae*t)-Fn*np.cos(omegae*t)*f)/Ic
    F = [f1, f2, f3, f4]
    for h in steps:
        T, Y_hist, K1_hist = RK4(F, t_0, Y0, h, tf=4)

        Y = np.vstack([Y_hist[0:2], K1_hist[1], Y_hist[2:], K1_hist[3]])

        scale_plot(
            T, Y,
            title  = f"RK4 com passo h = {h} e k1 = k2 = {k1} N/m2",
            ylabel = "$x, \\dot{x}, \\ddot{x}, \\theta, \\dot{\\theta}, \\ddot{\\theta}$ (SI × 10^x)",
            xlabel = "Tempo (s)",
            legend = ['x', 'xp', 'xpp', 'theta', 'thetap', 'thetapp']
            #legend = ['x', 'xp', 'theta', 'thetap', 'xpp', 'thetapp']
        )
