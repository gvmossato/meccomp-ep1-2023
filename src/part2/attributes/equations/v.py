# ==================================================== #
# Parameters of the vertical component of the velocity #
# potential gradient (and also the opposite of the     #
# horizontal component of the flow stream function)    #
# ==================================================== #

def blue(T, n):
    return [
        0, # j
        0, # j+2
        0, # j+1
        0, # j-1
        0, # j-2
    ]

def gray(T, n):
    return [
        0,                # i
        0,                # i+2
        -1 / (2 * T.h_x), # i+1
        1 / (2 * T.h_x),  # i-1
        0,                # i-2
    ]

def yellow(T, n):
    return [
        2 / (T.h_x * (n.a - 1)),  # i
        0,                        # i+2
        -1 / (T.h_x * (n.a - 1)), # i+1
        -1 / (T.h_x * (n.a - 1)), # i-1
        0,                        # i-2
    ]

def red(T, n):
    return [
        -2 / (T.h_x * (n.a - 1)), # i
        0,                        # i+2
        1 / (T.h_x * (n.a - 1)),  # i+1
        1 / (T.h_x * (n.a - 1)),  # i-1
        0,                        # i-2
    ]