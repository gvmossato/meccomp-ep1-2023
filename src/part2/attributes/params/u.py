# ====================================================== #
# Parameters of the horizontal component of the velocity #
# potential gradient (and also the vertical component of #
# the flow stream function)                              #
# ====================================================== #

import numpy as np

import src.part2.attributes.equations.u as eq


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
    100.0 / 3.6, # Rosa
    0.0,         # Rosa
    0.0,         # Cinza
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
    },
    "br": {
        "color": "#0000FF", # Azul
        "coeffs": lambda T, n: eq.blue(T, n),
    },
    "b": {
        "color": "#0000FF", # Azul
        "coeffs": lambda T, n: eq.blue(T, n),
    },
}

colors = [
    "#FF00D0", # Rosa
    "#FF00D0", # Rosa
    "#A7A7A7", # Cinza
]
