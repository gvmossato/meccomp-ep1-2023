# ====================================================== #
# Equations of the horizontal component of the heat flux #
# ====================================================== #

def pink(T, n):
    return [
        0, # j
        0, # j+2
        0, # j+1
        0, # j-1
        0, # j-2
    ]

def gray(T, n):
    return [
          0,             # j
          0,             # j+2
        - T.k/(2*T.h_y), # j+1
        + T.k/(2*T.h_y), # j-1
          0,             # j-2
    ]

def blue(T, n):
    return [
        - 2*T.k/(T.h_y*(n.b - 1)), # j
          0,                       # j+2
        + T.k/(T.h_y*(n.b - 1)),   # j+1
        + T.k/(T.h_y*(n.b - 1)),   # j-1
          0,                       # j-2
    ]
