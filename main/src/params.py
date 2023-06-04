# =================================== #
# Consolidação de todos os parâmetros #
# =================================== #

import main.store.V_params as V

voltage_params = {
    "regions"  : V.regions,
    "coeffs"   : V.coeffs,
    "initials" : V.initials,
    "irregs"   : V.irregs,
    "corners"  : V.corners,
    "colors"   : V.colors,
}

params = {
    "V": voltage_params,
}
