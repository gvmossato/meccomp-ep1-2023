# ============================== #
# Flow stream function equations #
# ============================== #

def blue(T, n):
    return [
        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j+1
        T.h_y**2 / (T.h_x**2 + T.h_y**2),       # i+1
        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j-1
        0,                                      # i-1
        0,                                      # indep
    ]

def pink(T, n):
    return [
        0,                                              # j+1
        T.h_y**2 / (2 * (T.h_x**2 + T.h_y**2)),         # i+1
        T.h_x**2 / (T.h_x**2 + T.h_y**2),               # j-1
        T.h_y**2 / (2 * (T.h_x**2 + T.h_y**2)),         # i-1
        T.h_x**2 * T.h_y * T.V / (T.h_x**2 + T.h_y**2), # indep
    ]

def green(T, n):
    return [
        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j+1
        0,                                      # i+1
        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j-1
        T.h_y**2 / (T.h_x**2 + T.h_y**2),       # i-1
        0,                                      # indep
    ]

def red(T, n):
    return [
        0, # j+1
        0, # i+1
        0, # j-1
        0, # i-1
        0, # indep
    ]

def gray(T, n):
    return [
        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j+1
        T.h_y**2 / (2 * (T.h_x**2 + T.h_y**2)), # i+1
        T.h_x**2 / (2 * (T.h_x**2 + T.h_y**2)), # j-1
        T.h_y**2 / (2 * (T.h_x**2 + T.h_y**2)), # i-1
        0,                                      # indep
    ]

def cyan(T, n):
    return [
        T.h_x**2 * n.a / (2 * (T.h_x**2*n.a + T.h_y**2)),       # j+1
        T.h_y**2 / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2)),       # i+1
        T.h_x**2 * n.a / (2 * (T.h_x**2*n.a + T.h_y**2)),       # j-1
        T.h_y**2 * n.a / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2)), # i-1
        0,                                                      # indep
    ]

def orange(T, n):
    return [
        T.h_x**2 * n.a * n.b / ((n.b+1) * (T.h_x**2*n.a + T.h_y**2*n.b)), # j+1
        T.h_y**2 * n.b / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2*n.b)),       # i+1
        T.h_x**2 * n.a / ((n.b+1) * (T.h_x**2*n.a + T.h_y**2*n.b)),       # j-1
        T.h_y**2 * n.a * n.b / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2*n.b)), # i-1
        0,                                                                # indep
    ]

def yellow(T, n):
    return [
        T.h_x**2 * n.b / ((n.b+1) * (T.h_x**2 + T.h_y**2*n.b)), # j+1
        T.h_y**2 * n.b / (2 * (T.h_x**2 + T.h_y**2*n.b)),       # i+1
        T.h_x**2 / ((n.b+1) * (T.h_x**2 + T.h_y**2*n.b)),       # j-1
        T.h_y**2 * n.b / (2 * (T.h_x**2 + T.h_y**2*n.b)),       # i-1
        0,                                                      # indep
    ]

def purple(T, n):
    return [
        T.h_x**2 * n.a * n.b / ((n.b+1) * (T.h_x**2*n.a + T.h_y**2*n.b)), # j+1
        T.h_y**2 * n.a * n.b / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2*n.b)), # i+1
        T.h_x**2 * n.a / ((n.b+1) * (T.h_x**2*n.a + T.h_y**2*n.b)),       # j-1
        T.h_y**2 * n.b / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2*n.b)),       # i-1
        0,                                                                # indep
    ]

def light_blue(T, n):
    return [
        T.h_x**2 * n.a / (2 * (T.h_x**2*n.a + T.h_y**2)),       # j+1
        T.h_y**2 * n.a / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2)), # i+1
        T.h_x**2 * n.a / (2 * (T.h_x**2*n.a + T.h_y**2)),       # j-1
        T.h_y**2 / ((n.a+1) * (T.h_x**2*n.a + T.h_y**2)),       # i-1
        0,                                                      # indep
    ]

def beige(T, n):
    return [
        0,                                              # j+1
        T.h_y**2 / (T.h_x**2 + T.h_y**2),               # i+1
        T.h_x**2 / (T.h_x**2 + T.h_y**2),               # j-1
        0,                                              # i-1
        T.h_x**2 * T.h_y * T.V / (T.h_x**2 + T.h_y**2), # indep
    ]

def brown(T, n):
    return [
        0,                                              # j+1
        0,                                              # i+1
        T.h_x**2 / (T.h_x**2 + T.h_y**2),               # j-1
        T.h_y**2 / (T.h_x**2 + T.h_y**2),               # i-1
        T.h_x**2 * T.h_y * T.V / (T.h_x**2 + T.h_y**2), # indep
    ]

def black(T, n):
    return [
        0, # j+1
        0, # i+1
        0, # j-1
        0, # i-1
        0, # indep
    ]
