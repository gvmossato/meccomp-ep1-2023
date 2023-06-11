# ============================= #
# Consolidate problem constants #
# ============================= #

import numpy as np


L = 3.0 # m

constants = {
    # Dimensions
    "L"      : L,                                          # m
    "d"      : 0.5*L,                                      # m
    "H"      : 2.0*L,                                      # m
    "r"      : 0.5*L,                                      # m
    "h_vals" : [0.5, 1.00, 1.50, 2.00, 2.50], # m

    # Air
    "V_vals" : np.array([75.0, 100.0, 140.0]) / 3.6, # m/s
    "rho"    : 1.25,                                 # kg/m^3
    "k"      : 0.026,                                # W/(m * K)
    "cp"     : 1002.0,                               # J/(kg * K)
    "gamma" : 1.4,

    # Temperature
    "T_in"     : 25.0 + 273.15, # K
    "T_out"    : 20.0 + 273.15, # K
    "T_engine" : 80.0 + 273.15, # K
}
