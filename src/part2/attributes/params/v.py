# ==================================================== #
# Parameters of the vertical component of the velocity #
# potential gradient (and also the opposite of the     #
# horizontal component of the flow stream function)    #
# ==================================================== #

import numpy as np

import src.part2.attributes.equations.v as eq


regions = np.array([
    [0.00, 0.00, 0.00, 6.00],           # Azul
    [6.00, 6.00, 0.00, 6.00],           # Azul
    [-np.inf, np.inf, -np.inf, np.inf], # Cinza
 ])

coeffs = [
    lambda T, n: eq.blue(T, n),
    lambda T, n: eq.blue(T, n),
    lambda T, n: eq.gray(T, n),
]

initials = [
    0.0, # Azul
    0.0, # Azul
    0.0, # Cinza
]

constant = [
    True, # Azul
    True, # Azul
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
    "#0000FF", # Azul
    "#A7A7A7", # Cinza
]
