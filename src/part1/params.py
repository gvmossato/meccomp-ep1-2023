# ============================= #
# Consolidate problem constants #
# ============================= #

import numpy as np


def d1(A, omega, t):
    return A*(1-np.cos(omega*t)) if t < 2 else 0

def d1p(A, omega, t):
    return A*omega*np.sin(omega*t) if t < 2 else 0

def d2(A, omega, t):
    return A*(1+np.cos(omega*t)) if t < 2 else 0

def d2p(A, omega, t):
    return -A*omega*np.sin(omega*t) if t < 2 else 0

k1 = 2.8e7    # N/m
c1 = 3e4      # N/m
vel = 50/3.6  # m/s
L = 0.5       # m
re = 0.045    # m
me = 20       # kg
fe = 2100/60  # rpm
omegae = 2*fe * np.pi

initials = {
    "t_0"      : 0.00, # s
    "theta_0"  : 0.09, # rad
    "x_0"      : 0.00, # m
    "xp_0"     : 0.00, # m
    "thetap_0" : 0.00, # rad
}

constants = {
    'M'      : 1783,    # Kg
    'a'      : 1220e-3, # m
    'b'      : 1500e-3, # m
    'Ic'     : 4000,    # kg * m2
    'e'      : 0.75,    # m
    'A'      : 60e-3,   # m
    'f'      : 0.35,    # m
    'k1'     : k1,      # N/m
    'k2'     : k1,      # N/m
    'c1'     : c1,      # Kg/s
    'c2'     : c1,      # Kg/s
    'L'      : L,       # m
    'vel'    : vel,     # m/s
    're'     : re,      # m
    'me'     : me,      # kg
    'fe'     : fe,      # rpm
    'omegae' : 2*fe * np.pi,
    'omega'  : 2*np.pi * vel / L,
    'Fn'     : me * omegae**2 * re
}
