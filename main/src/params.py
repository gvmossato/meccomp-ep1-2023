# =================================== #
# Consolidação de todos os parâmetros #
# =================================== #

import main.store.C_params as C
import main.store.u_params as u
import main.store.v_params as v
import main.store.T_params as T
import main.store.z_params as z
import main.store.w_params as w


C_params = {
    "regions"  : C.regions,
    "coeffs"   : C.coeffs,
    "initials" : C.initials,
    "constant" : C.constant,
    "irregs"   : C.irregs,
    "corners"  : C.corners,
    "colors"   : C.colors,
}

u_params = {
    "regions"  : u.regions,
    "coeffs"   : u.coeffs,
    "initials" : u.initials,
    "constant" : u.constant,
    "irregs"   : u.irregs,
    "colors"   : u.colors,
}

v_params = {
    "regions"  : v.regions,
    "coeffs"   : v.coeffs,
    "initials" : v.initials,
    "constant" : v.constant,
    "irregs"   : v.irregs,
    "colors"   : v.colors,
}

T_params = {
    "regions"  : T.regions,
    "coeffs"   : T.coeffs,
    "initials" : T.initials,
    "constant" : T.constant,
    "irregs"   : T.irregs,
    "corners"  : T.corners,
    "colors"   : T.colors,
}

z_params = {
    "regions"  : z.regions,
    "coeffs"   : z.coeffs,
    "initials" : z.initials,
    "constant" : z.constant,
    "irregs"   : z.irregs,
    "colors"   : z.colors,
}

w_params = {
    "regions"  : w.regions,
    "coeffs"   : w.coeffs,
    "initials" : w.initials,
    "constant" : w.constant,
    "irregs"   : w.irregs,
    "colors"   : w.colors,
}

params = {
    "C": C_params,
    "u": u_params,
    "v": v_params,
    "T": T_params,
    "z": z_params,
    "w": w_params,
}
