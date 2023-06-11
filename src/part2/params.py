# ================================= #
# Consolidate attributes parameters #
# ================================= #

import src.part2.attributes.params.C as C
import src.part2.attributes.params.u as u
import src.part2.attributes.params.v as v
import src.part2.attributes.params.T as T
import src.part2.attributes.params.z as z
import src.part2.attributes.params.w as w


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
