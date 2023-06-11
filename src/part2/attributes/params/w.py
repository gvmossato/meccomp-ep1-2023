# ======================================================= #
# Parameters of the horizontal component of the heat flux #
# ======================================================= #

import numpy as np

import src.part2.attributes.equations.w as eq


regions = np.array([
    [0.00, 6.00, 6.00, 6.00],           # Rosa
    [0.00, 6.00, 0.00, 0.00],           # Rosa
    [-np.inf, np.inf, -np.inf, np.inf], # Cinza
 ])

coeffs = [
    lambda T, n: eq.pink(T, n),
    lambda T, n: eq.pink(T, n),
    lambda T, n: eq.gray(T, n),
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
        "coeffs": lambda T, n: eq.blue(T, n),
        "initial": 0.0,
        "constant": False,
    },
    "br": {
        "color": "#0000FF", # Azul
        "coeffs": lambda T, n: eq.blue(T, n),
        "initial": 0.0,
        "constant": False,
    },
    "b": {
        "color": "#0000FF", # Azul
        "coeffs": lambda T, n: eq.blue(T, n),
        "initial": 0.0,
        "constant": False,
    },
}

colors = [
    "#FF00D0", # Rosa
    "#FF00D0", # Rosa
    "#A7A7A7", # Cinza
]
