# ==================== #
# Parâmetros de tensão #
# ==================== #

import numpy as np

from main.store.eqns import *

regions = np.array([
    [0.00, 0.00, 0.00, 6.00],           # Azul
    [0.00, 6.00, 6.00, 6.00],           # Rosa
    [6.00, 6.00, 0.00, 6.00],           # Verde
    [0.00, 6.00, 0.00, 0.00],           # Vermelho
    [-np.inf, np.inf, -np.inf, np.inf], # Cinza
 ])

coeffs = [
    lambda T, n: [ # Azul
        0.0, # j+1
        0.0, # i+1
        0.0, # j-1
        0.0, # i-1
        0.0, # indep
    ],
    lambda T, n: pink(T, n), # Rosa
    lambda T, n: green(T, n), # Verde
    lambda T, n: red(T, n), # Vermelho
    lambda T, n: gray(T, n), # Cinza
]

initials = [
    293.15, # Azul
    0.0, # Rosa
    0.0, # Verde
    0.0, # Vermelho
    0.0, # Cinza
]

constant = [
    True, # Azul
    False, # Rosa
    False, # Verde
    False,  # Vermelho
    False, # Cinza
]

irregs = {
    "r": {
        "color": "#00DDFF", # Ciano
        "coeffs": lambda T, n: cyan(T, n),
    },
    "br": {
        "color": "#FF8800", # Laranja
        "coeffs": lambda T, n: [
            - T.h_x**2*n.a*n.b*(n.a - 1)*(T.h_y*n.b*T.cp*T.rho*n.v['value'] + T.h_y*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/(2*(n.b + 1)*(-T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*n.a**2*n.b*T.k + T.h_x**2*n.a**2*T.k + T.h_x**2*n.a*n.b*T.k - T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] - T.h_y**2*n.a*n.b**2*T.k + T.h_y**2*n.a*n.b*T.k + T.h_y**2*n.b**2*T.k - T.h_y**2*n.b*T.k)),    # j+1
            + T.h_y**2*n.b*(n.b - 1)*(T.h_x*n.a**2*T.cp*T.rho*n.u['value'] + T.h_x*n.a*T.cp*T.rho*n.u['value'] - 2*n.a*T.k + 2*T.k)/(2*(n.a + 1)*(-T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*n.a**2*n.b*T.k + T.h_x**2*n.a**2*T.k + T.h_x**2*n.a*n.b*T.k - T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] - T.h_y**2*n.a*n.b**2*T.k + T.h_y**2*n.a*n.b*T.k + T.h_y**2*n.b**2*T.k - T.h_y**2*n.b*T.k)), # i+1
            - T.h_x**2*n.a*(n.a - 1)*(T.h_y*n.b**2*T.cp*T.rho*n.v['value'] + T.h_y*n.b*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/(2*(n.b + 1)*(-T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*n.a**2*n.b*T.k + T.h_x**2*n.a**2*T.k + T.h_x**2*n.a*n.b*T.k - T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] - T.h_y**2*n.a*n.b**2*T.k + T.h_y**2*n.a*n.b*T.k + T.h_y**2*n.b**2*T.k - T.h_y**2*n.b*T.k)), # j-1
            + T.h_y**2*n.a*n.b*(n.b - 1)*(T.h_x*n.a*T.cp*T.rho*n.u['value'] + T.h_x*T.cp*T.rho*n.u['value'] - 2*n.a*T.k + 2*T.k)/(2*(n.a + 1)*(-T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*n.a**2*n.b*T.k + T.h_x**2*n.a**2*T.k + T.h_x**2*n.a*n.b*T.k - T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] - T.h_y**2*n.a*n.b**2*T.k + T.h_y**2*n.a*n.b*T.k + T.h_y**2*n.b**2*T.k - T.h_y**2*n.b*T.k)),    # i-1
            0.0,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          # indep
        ],
    },
    "b": {
        "color": "#FFFF00", # Amarelo
        "coeffs": lambda T, n: yellow(T, n),
    },
    "bl": {
        "color": "#BB00FF", # Roxo
        "coeffs": lambda T, n: [
            + T.h_x**2*n.a*n.b*(n.a - 1)*(T.h_y*n.b*T.cp*T.rho*n.v['value'] + T.h_y*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/(2*(n.b + 1)*(T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*n.a**2*n.b*T.k - T.h_x**2*n.a**2*T.k - T.h_x**2*n.a*n.b*T.k + T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] + T.h_y**2*n.a*n.b**2*T.k - T.h_y**2*n.a*n.b*T.k - T.h_y**2*n.b**2*T.k + T.h_y**2*n.b*T.k)),    # j+1
            + T.h_y**2*n.a*n.b*(n.b - 1)*(T.h_x*n.a*T.cp*T.rho*n.u['value'] + T.h_x*T.cp*T.rho*n.u['value'] + 2*n.a*T.k - 2*T.k)/(2*(n.a + 1)*(T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*n.a**2*n.b*T.k - T.h_x**2*n.a**2*T.k - T.h_x**2*n.a*n.b*T.k + T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] + T.h_y**2*n.a*n.b**2*T.k - T.h_y**2*n.a*n.b*T.k - T.h_y**2*n.b**2*T.k + T.h_y**2*n.b*T.k)),    # i+1
            + T.h_x**2*n.a*(n.a - 1)*(T.h_y*n.b**2*T.cp*T.rho*n.v['value'] + T.h_y*n.b*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/(2*(n.b + 1)*(T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*n.a**2*n.b*T.k - T.h_x**2*n.a**2*T.k - T.h_x**2*n.a*n.b*T.k + T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] + T.h_y**2*n.a*n.b**2*T.k - T.h_y**2*n.a*n.b*T.k - T.h_y**2*n.b**2*T.k + T.h_y**2*n.b*T.k)), # j-1
            + T.h_y**2*n.b*(n.b - 1)*(T.h_x*n.a**2*T.cp*T.rho*n.u['value'] + T.h_x*n.a*T.cp*T.rho*n.u['value'] + 2*n.a*T.k - 2*T.k)/(2*(n.a + 1)*(T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*n.a**2*n.b*T.k - T.h_x**2*n.a**2*T.k - T.h_x**2*n.a*n.b*T.k + T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] + T.h_y**2*n.a*n.b**2*T.k - T.h_y**2*n.a*n.b*T.k - T.h_y**2*n.b**2*T.k + T.h_y**2*n.b*T.k)), # i-1
            0.0,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         # indep
        ],
    },
    "l": {
        "color": "#82AEFF", # Azul Claro
        "coeffs": lambda T, n: light_blue(T, n),
    },
}

corners = {
    'tl': {
        "color": "#000000", # Preto
        "coeffs": lambda T, n: [
            0.0, # j+1
            0.0, # i+1
            0.0, # j-1
            0.0, # i-1
            0.0, # indep
        ],
        "constant": True,
        "initial": 293.15,
    },
    'tr': {
        "color": "#804800", # Marrom
        "coeffs": lambda T, n: [
            0.0,                                # j+1
            0.0,                                # i+1
            + T.h_x**2/(T.h_x**2 + T.h_y**2), # j-1
            + T.h_y**2/(T.h_x**2 + T.h_y**2), # i-1
            0.0,                                # indep
        ],
        "constant": False,
        "initial": 0.0,
    },
    'br': {
        "color": "#C9B389", # Beje
        "coeffs": lambda T, n: [
            + T.h_x**2/(T.h_x**2 + T.h_y**2), # j+1
            0.0,                                # i+1
            0.0,                                # j-1
            + T.h_y**2/(T.h_x**2 + T.h_y**2), # i-1
            0.0,                                # indep
        ],
        "constant": False,
        "initial": 0.0,
    },
    'bl': {
        "color": "#000000", # Preto
        "coeffs": lambda T, n: [
            0.0, # j+1
            0.0, # i+1
            0.0, # j-1
            0.0, # i-1
            0.0, # indep
        ],
        "constant": True,
        "initial": 293.15,
    }
}

colors = [
    "#0000FF", # Azul
    "#FF00D0", # Rosa
    "#00FF00", # Verde
    "#FF0000", # Vermelho
    "#A7A7A7", # Cinza
]
