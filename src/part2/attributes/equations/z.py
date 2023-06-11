# ==================================================== #
# Equations of the vertical component of the heat flux #
# ==================================================== #

def blue(T, n):
    return [
        + 3*T.k/(2*T.h_x), # i
        + T.k/(2*T.h_x),   # i+2
        - 2*T.k/T.h_x,     # i+1
          0,               # i-1
          0,               # i-2
    ]

def green(T, n):
    return [
        0, # i
        0, # i+2
        0, # i+1
        0, # i-1
        0, # i-2
    ]

def gray(T, n):
    return [
        0,               # i
        0,               # i+2
        - T.k/(2*T.h_x), # i+1
        + T.k/(2*T.h_x), # i-1
        0,               # i-2
    ]

def yellow(T, n):
    return [
        + 2*T.k/(T.h_x*(n.a - 1)), # i
            0,                     # i+2
        - T.k/(T.h_x*(n.a - 1)),   # i+1
        - T.k/(T.h_x*(n.a - 1)),   # i-1
            0,                     # i-2
    ]

def red(T, n):
    return [
        - 2*T.k/(T.h_x*(n.a - 1)), # i
            0,                     # i+2
        + T.k/(T.h_x*(n.a - 1)),   # i+1
        + T.k/(T.h_x*(n.a - 1)),   # i-1
            0,                     # i-2
    ]
