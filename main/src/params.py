# =================================== #
# Consolidação de todos os parâmetros #
# =================================== #

import main.store.C_params as C
import main.store.u_params as u
import main.store.v_params as v


current_params = {
    "regions"  : C.regions,
    "coeffs"   : C.coeffs,
    "initials" : C.initials,
    "irregs"   : C.irregs,
    "corners"  : C.corners,
    "colors"   : C.colors,
}

u_params = {
    "regions"  : u.regions,
    "coeffs"   : u.coeffs,
    "initials" : u.initials,
    "irregs"   : u.irregs,
    "colors"   : u.colors,
}

v_params = {
    "regions"  : v.regions,
    "coeffs"   : v.coeffs,
    "initials" : v.initials,
    "irregs"   : v.irregs,
    "colors"   : v.colors,
}

params = {
    "C": current_params,
    "u": u_params,
    "v": v_params,
}
