# ==================== #
# Parâmetros de tensão #
# ==================== #

import numpy as np

regions = np.array([
    [0.00, 0.00, 0.00, 6.00],           # Azul
    [6.00, 6.00, 0.00, 6.00],           # Verde
    [-np.inf, np.inf, -np.inf, np.inf], # Cinza
 ])

coeffs = [
    lambda T, n: [  # Azul
        + 3*T.k/(2*T.h_x), # i
        + T.k/(2*T.h_x),   # i+2
        - 2*T.k/T.h_x,     # i+1
        0,               # i-1
        0,               # i-2
    ],
    lambda T, n: [  # Verde
        0, # i
        0, # i+2
        0, # i+1
        0, # i-1
        0, # i-2
    ],
    lambda T, n: [        # Cinza
        0,             # i
        0,             # i+2
        - T.k/(2*T.h_x), # i+1
        + T.k/(2*T.h_x), # i-1
        0,             # i-2
    ],
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
        "coeffs": lambda T, n: [
            + 2*T.k/(T.h_x*(n.a - 1)), # i
              0,                     # i+2
            - T.k/(T.h_x*(n.a - 1)), # i+1
            - T.k/(T.h_x*(n.a - 1)), # i-1
              0,                     # i-2
        ],
    },
    "bl": {
        "color": "#FF0000", # Vermelho
        "coeffs": lambda T, n: [
            - 2*T.k/(T.h_x*(n.a - 1)), # i
              0,                     # i+2
            + T.k/(T.h_x*(n.a - 1)), # i+1
            + T.k/(T.h_x*(n.a - 1)), # i-1
              0,                     # i-2
        ],
    },
    "r": {
        "color": "#FFFF00", # Amarelo
        "coeffs": lambda T, n: [
            + 2*T.k/(T.h_x*(n.a - 1)), # i
              0,                     # i+2
            - T.k/(T.h_x*(n.a - 1)), # i+1
            - T.k/(T.h_x*(n.a - 1)), # i-1
              0,                     # i-2
        ],
    },
    "l": {
        "color": "#FF0000", # Vermelho
        "coeffs": lambda T, n: [
            - 2*T.k/(T.h_x*(n.a - 1)), # i
              0,                     # i+2
            + T.k/(T.h_x*(n.a - 1)), # i+1
            + T.k/(T.h_x*(n.a - 1)), # i-1
              0,                     # i-2
        ],
    },
}

colors = [
    "#0000FF", # Azul
    "#00FF00", # Verde
    "#A7A7A7", # Cinza
]
