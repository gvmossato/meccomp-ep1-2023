import numpy as np

from src.utils import ctext
from src.part1.lib import RK4, scale_plot
from src.part1.params import initials, constants, d1, d2, d1p, d2p


global vel, k1, k2, c1, c2

M = constants["M"]
k1 = constants["k1"]
k2 = constants["k2"]
c1 = constants["c1"]
c2 = constants["c2"]
a = constants["a"]
b = constants["b"]
Ic = constants["Ic"]
e = constants["e"]
L = constants["L"]
A = constants["A"]
f = constants["f"]
vel = constants["vel"]
re = constants["re"]
me = constants["me"]
fe = constants["fe"]
omegae = constants["omegae"]
Fn = constants["Fn"]
omega = constants["omega"]

t = initials["t_0"]
x = initials["x_0"]
xp = initials["xp_0"]
theta = initials["theta_0"]
thetap = initials["thetap_0"]
Y0 = [x, xp, theta, thetap]


def run_a():
    F = [
        lambda t, Y: (Y[1]),
        lambda t, Y: ((-k1*(Y[0]-a*Y[2]-d1(A, omega, t))-k2*(Y[0]+b*Y[2]-d2(A, omega, t))-c1*(Y[1]-a*Y[3]-d1p(A,omega,t))-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))+Fn*np.sin(omegae*t))/M),
        lambda t, Y: Y[3],
        lambda t, Y: (k1*(Y[0]-a*Y[2]-d1(A, omega,t))*a-k2*(Y[0]+b*Y[2]-d2(A,omega,t))*b+c1*(Y[1]-a*Y[3]-d1p(A,omega,t))*a-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))*b-Fn*np.sin(omegae*t)-Fn*np.cos(omegae*t)*f)/Ic
    ]

    steps = [1e-2, 1e-4, 1e-5]

    for h in steps:
        print(f"\nCalculando para {ctext(f'h={h}', 'g')}...")

        T, Y_hist, K1_hist = RK4(F, t, Y0, h, tf=4)

        Y = np.vstack([Y_hist[0:2], K1_hist[1], Y_hist[2:], K1_hist[3]])

        scale_plot(
            T, Y,
            title  = f"RK4 com passo h = {h}",
            ylabel = "$x, \\dot{x}, \\ddot{x}, \\theta, \\dot{\\theta}, \\ddot{\\theta}$ (SI × 10^x)",
            xlabel = "Tempo (s)",
            legend = ['x', 'dx/dt', 'd²x/dt²', 'θ', 'dθ/dt', 'd²θ/dt²']
        )


def run_b():
    global vel, k1, k2, c1, c2

    step = 1e-4

    # b. i)
    print("\nExecutando testes de velocidades...")

    for vel in [30.0/3.6, 70.0/3.6]:
        omega = 2*np.pi * vel  /L

        F = [
            lambda t, Y: (Y[1]),
            lambda t, Y: ((-k1*(Y[0]-a*Y[2]-d1(A, omega, t))-k2*(Y[0]+b*Y[2]-d2(A, omega, t))-c1*(Y[1]-a*Y[3]-d1p(A,omega,t))-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))+Fn*np.sin(omegae*t))/M),
            lambda t, Y: Y[3],
            lambda t, Y: (k1*(Y[0]-a*Y[2]-d1(A, omega,t))*a-k2*(Y[0]+b*Y[2]-d2(A,omega,t))*b+c1*(Y[1]-a*Y[3]-d1p(A,omega,t))*a-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))*b-Fn*np.sin(omegae*t)-Fn*np.cos(omegae*t)*f)/Ic
        ]

        T, Y_hist, K1_hist = RK4(F, t, Y0, h=step, tf=4)
        Y = np.vstack([Y_hist[0:2], K1_hist[1], Y_hist[2:], K1_hist[3]])

        scale_plot(
            T, Y,
            title  = f"RK4 com passo h = {step} e velocidade V = {vel*3.6:.2f} km/h",
            ylabel = "$x, \\dot{x}, \\ddot{x}, \\theta, \\dot{\\theta}, \\ddot{\\theta}$ (SI × 10^x)",
            xlabel = "Tempo (s)",
            legend = ['x', 'dx/dt', 'd²x/dt²', 'θ', 'dθ/dt', 'd²θ/dt²']
        )

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    # Resets values
    vel = 50/3.6
    omega = 2*np.pi * vel / L

    # b. ii)
    print('\033[F', end='')
    print("Executando testes de amortecimento...            ")

    for c1 in [1e3, 5e4, 2.5e5]:
        c2 = c1

        F = [
            lambda t, Y: (Y[1]),
            lambda t, Y: ((-k1*(Y[0]-a*Y[2]-d1(A, omega, t))-k2*(Y[0]+b*Y[2]-d2(A, omega, t))-c1*(Y[1]-a*Y[3]-d1p(A,omega,t))-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))+Fn*np.sin(omegae*t))/M),
            lambda t, Y: Y[3],
            lambda t, Y: (k1*(Y[0]-a*Y[2]-d1(A, omega,t))*a-k2*(Y[0]+b*Y[2]-d2(A,omega,t))*b+c1*(Y[1]-a*Y[3]-d1p(A,omega,t))*a-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))*b-Fn*np.sin(omegae*t)-Fn*np.cos(omegae*t)*f)/Ic
        ]

        T, Y_hist, K1_hist = RK4(F, t, Y0, step, tf=4)
        Y = np.vstack([Y_hist[0:2], K1_hist[1], Y_hist[2:], K1_hist[3]])

        scale_plot(
            T, Y,
            title  = f"RK4 com passo h = {step} e c1 = c2 = {c1} kg/s",
            ylabel = "$x, \\dot{x}, \\ddot{x}, \\theta, \\dot{\\theta}, \\ddot{\\theta}$ (SI × 10^x)",
            xlabel = "Tempo (s)",

            legend = ['x', 'dx/dt', 'd²x/dt²', 'θ', 'dθ/dt', 'd²θ/dt²']
        )

    input(f"\nPressione {ctext('ENTER', 'g')} para continuar")

    # Resets values
    c1 = c2 = 3e4

    # b. iii)
    print('\033[F', end='')
    print("Executando testes de molas...                  \n")

    for k1 in [2e4, 5e6, 7e8]:
        k2 = k1

        F = [
            lambda t, Y: (Y[1]),
            lambda t, Y: ((-k1*(Y[0]-a*Y[2]-d1(A, omega, t))-k2*(Y[0]+b*Y[2]-d2(A, omega, t))-c1*(Y[1]-a*Y[3]-d1p(A,omega,t))-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))+Fn*np.sin(omegae*t))/M),
            lambda t, Y: Y[3],
            lambda t, Y: (k1*(Y[0]-a*Y[2]-d1(A, omega,t))*a-k2*(Y[0]+b*Y[2]-d2(A,omega,t))*b+c1*(Y[1]-a*Y[3]-d1p(A,omega,t))*a-c2*(Y[1]+b*Y[3]-d2p(A,omega,t))*b-Fn*np.sin(omegae*t)-Fn*np.cos(omegae*t)*f)/Ic
        ]

        T, Y_hist, K1_hist = RK4(F, t, Y0, step, tf=4)
        Y = np.vstack([Y_hist[0:2], K1_hist[1], Y_hist[2:], K1_hist[3]])

        scale_plot(
            T, Y,
            title  = f"RK4 com passo h = {step} e k1 = k2 = {k1} N/m2",
            ylabel = "$x, \\dot{x}, \\ddot{x}, \\theta, \\dot{\\theta}, \\ddot{\\theta}$ (SI × 10^x)",
            xlabel = "Tempo (s)",
            legend = ['x', 'dx/dt', 'd²x/dt²', 'θ', 'dθ/dt', 'd²θ/dt²']
        )


def solve(item):
    if item == 'a': run_a()
    else: run_b()
