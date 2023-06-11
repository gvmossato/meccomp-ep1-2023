# ===================================================== #
# Parameters of the vertical component of the heat flux #
# ===================================================== #

import numpy as np

import src.part2.attributes.equations.z as eq


regions = np.array([
    [0.00, 0.00, 0.00, 6.00],           # Azul
    [6.00, 6.00, 0.00, 6.00],           # Verde
    [-np.inf, np.inf, -np.inf, np.inf], # Cinza
 ])

coeffs = [
    lambda T, n: eq.blue(T, n),
    lambda T, n: eq.green(T, n),
    lambda T, n: eq.gray(T, n),
]

initials = [
    0.0, # Azul
    0.0, # Verde
    0.0, # Cinza
]

constant = [
    False, # Azul
    True, # Verde
    False, # Cinza
]

irregs = {
    "br": {
        "color": "#FFFF00", # Amarelo
        "coeffs": lambda T, n: eq.yellow(T, n),
    },
    "bl": {
        "color": "#FF0000", # Vermelho
        "coeffs": lambda T, n: eq.red(T, n),
    },
    "r": {
        "color": "#FFFF00", # Amarelo
        "coeffs": lambda T, n: eq.yellow(T, n),
    },
    "l": {
        "color": "#FF0000", # Vermelho
        "coeffs": lambda T, n: eq.red(T, n),
    },
}

colors = [
    "#0000FF", # Azul
    "#00FF00", # Verde
    "#A7A7A7", # Cinza
]
