# ==================== #
# Parâmetros de tensão #
# ==================== #

import numpy as np

regions = np.array([
    [0.00, 6.00, 6.00, 6.00],           # Rosa
    [0.00, 6.00, 0.00, 0.00],           # Vermelho
    [-np.inf, np.inf, -np.inf, np.inf], # Cinza
 ])

coeffs = [
    lambda T, n: [  # Rosa
        3 / (2*T.h_y), # j
        0,             # j+2
        0,             # j+1
        -2 / T.h_y,    # j-1
        1 / (2*T.h_y), # j-2
    ],
    lambda T, n: [  # Vermelho
        -3 / (2*T.h_y), # j
        -1 / (2*T.h_y), # j+2
        2 / T.h_y,      # j+1
        0,              # j-1
        0,              # j-2
    ],
    lambda T, n: [        # Cinza
        0,                # j
        0,                # j+2
        1 / (2 * T.h_y),  # j+1
        -1 / (2 * T.h_y), # j-1
        0,                # j-2
    ],
]

initials = [
    0.0, # Rosa
    0.0, # Vermelho
    0.0, # Cinza
]

irregs = {
    # Any irregular combination that contains bottom should be handled as the same
    "bl": {
        "color": "#0000FF", # Azul
        "coeffs": lambda T, n: [
            0,                # j
            0,                # j+2
            1 / (2 * T.h_y),  # j+1
            -1 / (2 * T.h_y), # j-1
            0,                # j-2
        ],
    },
    "br": {
        "color": "#0000FF", # Azul
        "coeffs": lambda T, n: [
            0,                # j
            0,                # j+2
            1 / (2 * T.h_y),  # j+1
            -1 / (2 * T.h_y), # j-1
            0,                # j-2
        ],
    },
    "b": {
        "color": "#0000FF", # Azul
        "coeffs": lambda T, n: [
            0,                # j
            0,                # j+2
            1 / (2 * T.h_y),  # j+1
            -1 / (2 * T.h_y), # j-1
            0,                # j-2
        ],
    },
}

colors = [
    "#FF00D0", # Rosa
    "#FF0000", # Vermelho
    "#A7A7A7", # Cinza
]
