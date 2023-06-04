# ==================== #
# Parâmetros de tensão #
# ==================== #

import numpy as np

regions = np.array([
    [0.00, 0.00, 0.00, 6.00],           # Azul
    [0.00, 6.00, 6.00, 6.00],           # Rosa
    [6.00, 6.00, 0.00, 6.00],           # Verde
    [0.00, 6.00, 0.00, 0.00],           # Vermelho
    [-np.inf, np.inf, -np.inf, np.inf], # Cinza
 ])

coeffs = [
    lambda T, n: [                              # Azul
        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j+1
        T.h_y**2 / (T.h_x**2 + T.h_y**2),       # i+1
        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j-1
        0,                                      # i-1
        0,                                      # indep
    ],
    lambda T, n: [                                      # Rosa
        0,                                              # j+1
        T.h_y**2 / (2 * (T.h_x**2 + T.h_y**2)),         # i+1
        T.h_x**2 / (T.h_x**2 + T.h_y**2),               # j-1
        T.h_y**2 / (2 * (T.h_x**2 + T.h_y**2)),         # i-1
        T.h_x**2 * T.h_y * T.V / (T.h_x**2 + T.h_y**2), # indep
    ],
    lambda T, n: [                              # Verde

        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j+1
        0,                                      # i+1
        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j-1
        T.h_y**2 / (T.h_x**2 + T.h_y**2),       # i-1
        0,                                      # indep
    ],
    lambda T, n: [ # Vermelho
        0,         # j+1
        0,         # i+1
        0,         # j-1
        0,         # i-1
        0,         # indep
    ],
    lambda T, n: [                              # Cinza
        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j+1
        T.h_y**2 / (2 * (T.h_x**2 + T.h_y**2)), # i+1
        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j-1
        T.h_y**2 / (2 * (T.h_x**2 + T.h_y**2)), # i-1
        0,                                      # indep
    ],
]

initials = [
    0.0, # Azul
    0.0, # Rosa
    0.0, # Verde
    0.0, # Vermelho
    0.0, # Cinza
]

irregs = {
    "r": {
        "color": "#00DDFF", # Ciano
        "coeffs": lambda T, n: [
            T.h_x**2 * n.a / (2 * (T.h_x**2*n.a + T.h_y**2)),       # j+1
            T.h_y**2 / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2)),       # i+1
            T.h_x**2 * n.a / (2 * (T.h_x**2*n.a + T.h_y**2)),       # j-1
            T.h_y**2 * n.a / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2)), # i-1
            0,                                                      # indep
        ],
    },
    "br": {
        "color": "#FF8800", # Laranja
        "coeffs": lambda T, n: [
            T.h_x**2 * n.a * n.b / ((n.b+1) * (T.h_x**2*n.a + T.h_y**2*n.b)), # j+1
            T.h_y**2 * n.b / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2*n.b)),       # i+1
            T.h_x**2 * n.a / ((n.b+1) * (T.h_x**2*n.a + T.h_y**2*n.b)),       # j-1
            T.h_y**2 * n.a * n.b / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2*n.b)), # i-1
            0,                                                                # indep
        ],
    },
    "b": {
        "color": "#FFFF00", # Amarelo
        "coeffs": lambda T, n: [
            T.h_x**2 * n.b / ((n.b+1) * (T.h_x**2 + T.h_y**2*n.b)), # j+1
            T.h_y**2 * n.b / (2 * (T.h_x**2 + T.h_y**2*n.b)),       # i+1
            T.h_x**2 / ((n.b+1) * (T.h_x**2 + T.h_y**2*n.b)),       # j-1
            T.h_y**2 * n.b / (2 * (T.h_x**2 + T.h_y**2*n.b)),       # i-1
            0,                                                      # indep
        ],
    },
    "bl": {
        "color": "#BB00FF", # Roxo
        "coeffs": lambda T, n: [
            T.h_x**2 * n.a * n.b / ((n.b+1) * (T.h_x**2*n.a + T.h_y**2*n.b)), # j+1
            T.h_y**2 * n.a * n.b / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2*n.b)), # i+1
            T.h_x**2 * n.a / ((n.b+1) * (T.h_x**2*n.a + T.h_y**2*n.b)),       # j-1
            T.h_y**2 * n.b / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2*n.b)),       # i-1
            0,                                                                # indep
        ],
    },
    "l": {
        "color": "#82AEFF", # Vinho
        "coeffs": lambda T, n: [
            T.h_x**2 * n.a / (2 * (T.h_x**2*n.a + T.h_y**2)),       # j+1
            T.h_y**2 * n.a / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2)), # i+1
            T.h_x**2 * n.a / (2 * (T.h_x**2*n.a + T.h_y**2)),       # j-1
            T.h_y**2 / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2)),       # i-1
            0,                                                      # indep
        ],
    },
}

corners = {
    'tl': {
        "color": "#C9B389", # Beje
        "coeffs": lambda T, n: [
            0,                                              # j+1
            T.h_y**2 / (T.h_x**2 + T.h_y**2),               # i+1
            T.h_x**2 / (T.h_x**2 + T.h_y**2),               # j-1
            0,                                              # i-1
            T.h_x**2 * T.h_y * T.V / (T.h_x**2 + T.h_y**2), # indep
        ],
    },
    'tr': {
        "color": "#804800", # Marrom
        "coeffs": lambda T, n: [
            0,                                              # j+1
            0,                                              # i+1
            T.h_x**2 / (T.h_x**2 + T.h_y**2),               # j-1
            T.h_y**2 / (T.h_x**2 + T.h_y**2),               # i-1
            T.h_x**2 * T.h_y * T.V / (T.h_x**2 + T.h_y**2), # indep
        ],
    },
    'br': {
        "color": "#000000", # Preto
        "coeffs": lambda T, n: [
            0, # j+1
            0, # i+1
            0, # j-1
            0, # i-1
            0, # indep
        ],
    },
    'bl': {
        "color": "#000000", # Preto
        "coeffs": lambda T, n: [
            0, # j+1
            0, # i+1
            0, # j-1
            0, # i-1
            0, # indep
        ],
    }
}

colors = [
    "#0000FF", # Azul
    "#FF00D0", # Rosa
    "#00FF00", # Verde
    "#FF0000", # Vermelho
    "#A7A7A7", # Cinza
]
