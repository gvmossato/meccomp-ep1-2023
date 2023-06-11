# ====================================================== #
# Equations of the horizontal component of the velocity  #
# potential gradient (and also the vertical component of #
# the flow stream function)                              #
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
        0,                # j
        0,                # j+2
        1 / (2 * T.h_y),  # j+1
        -1 / (2 * T.h_y), # j-1
        0,                # j-2
    ]

def blue(T, n):
    return [
        2 / (T.h_y * (n.b - 1)),  # j
        0,                        # j+2
        -1 / (T.h_y * (n.b - 1)), # j+1
        -1 / (T.h_y * (n.b - 1)), # j-1
        0,                        # j-2
    ]
