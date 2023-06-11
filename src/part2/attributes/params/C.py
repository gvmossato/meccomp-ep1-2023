# =============================== #
# Flow stream function parameters #
# =============================== #

import numpy as np

import src.part2.attributes.equations.C as eq


regions = np.array([
    [0.00, 0.00, 0.00, 6.00],           # Azul
    [0.00, 6.00, 6.00, 6.00],           # Rosa
    [6.00, 6.00, 0.00, 6.00],           # Verde
    [0.00, 6.00, 0.00, 0.00],           # Vermelho
    [-np.inf, np.inf, -np.inf, np.inf], # Cinza
 ])

coeffs = [
    lambda T, n: eq.blue(T, n),
    lambda T, n: eq.pink(T, n),
    lambda T, n: eq.green(T, n),
    lambda T, n: eq.red(T, n),
    lambda T, n: eq.gray(T, n),
]

initials = [
    0.0, # Azul
    0.0, # Rosa
    0.0, # Verde
    0.0, # Vermelho
    0.0, # Cinza
]

constant = [
    False, # Azul
    False, # Rosa
    False, # Verde
    True,  # Vermelho
    False, # Cinza
]

irregs = {
    "r": {
        "color": "#00DDFF", # Ciano
        "coeffs": lambda T, n: eq.cyan(T, n),
    },
    "br": {
        "color": "#FF8800", # Laranja
        "coeffs": lambda T, n: eq.orange(T, n),
    },
    "b": {
        "color": "#FFFF00", # Amarelo
        "coeffs": lambda T, n: eq.yellow(T, n),
    },
    "bl": {
        "color": "#BB00FF", # Roxo
        "coeffs": lambda T, n: eq.purple(T, n),
    },
    "l": {
        "color": "#82AEFF", # Azul Claro
        "coeffs": lambda T, n: eq.light_blue(T, n),
    },
}

corners = {
    'tl': {
        "color": "#C9B389", # Beje
        "coeffs": lambda T, n: eq.beige(T, n),
        "constant": False,
        "initial": 0,
    },
    'tr': {
        "color": "#804800", # Marrom
        "coeffs": lambda T, n: eq.brown(T, n),
        "constant": False,
        "initial": 0,
    },
    'br': {
        "color": "#000000", # Preto
        "coeffs": lambda T, n: eq.black(T, n),
        "constant": True,
        "initial": 0,
    },
    'bl': {
        "color": "#000000", # Preto
        "coeffs": lambda T, n: eq.black(T, n),
        "constant": True,
        "initial": 0,
    }
}

colors = [
    "#0000FF", # Azul
    "#FF00D0", # Rosa
    "#00FF00", # Verde
    "#FF0000", # Vermelho
    "#A7A7A7", # Cinza
]
