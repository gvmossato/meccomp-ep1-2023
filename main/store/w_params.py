# ==================== #
# Parâmetros de tensão #
# ==================== #

import numpy as np

regions = np.array([
    [0.00, 6.00, 6.00, 6.00],           # Rosa
    [0.00, 6.00, 0.00, 0.00],           # Rosa
    [-np.inf, np.inf, -np.inf, np.inf], # Cinza
 ])

coeffs = [
    lambda T, n: [ # Rosa
        0,         # j
        0,         # j+2
        0,         # j+1
        0,         # j-1
        0,         # j-2
    ],
    lambda T, n: [ # Rosa
        0,         # j
        0,         # j+2
        0,         # j+1
        0,         # j-1
        0,         # j-2
    ],
    lambda T, n: [       # Cinza
          0,             # j
          0,             # j+2
        - T.k/(2*T.h_y), # j+1
        + T.k/(2*T.h_y), # j-1
          0,             # j-2
    ],
]

initials = [
    0.0, # Rosa
    0.0, # Rosa
    0.0, # Cinza
]

constant = [
    True,  # Rosa
    True,  # Rosa
    False, # Cinza
]

irregs = {
    # Any irregular combination that contains bottom should be handled as the same
    "bl": {
        "color": "#0000FF", # Azul
        "coeffs": lambda T, n: [
            - 2*T.k/(T.h_y*(n.b - 1)), # j
              0,                       # j+2
            + T.k/(T.h_y*(n.b - 1)),   # j+1
            + T.k/(T.h_y*(n.b - 1)),   # j-1
              0,                       # j-2
        ],
        "initial": 0.0,
        "constant": False,
    },
    "br": {
        "color": "#0000FF", # Azul
        "coeffs": lambda T, n: [
            - 2*T.k/(T.h_y*(n.b - 1)), # j
              0,                       # j+2
            + T.k/(T.h_y*(n.b - 1)),   # j+1
            + T.k/(T.h_y*(n.b - 1)),   # j-1
              0,                       # j-2
        ],
        "initial": 0.0,
        "constant": False,
    },
    "b": {
        "color": "#0000FF", # Azul
        "coeffs": lambda T, n: [
            - 2*T.k/(T.h_y*(n.b - 1)), # j
              0,                       # j+2
            + T.k/(T.h_y*(n.b - 1)),   # j+1
            + T.k/(T.h_y*(n.b - 1)),   # j-1
              0,                       # j-2
        ],
        "initial": 0.0,
        "constant": False,
    },
}

colors = [
    "#FF00D0", # Rosa
    "#FF00D0", # Rosa
    "#A7A7A7", # Cinza
]
