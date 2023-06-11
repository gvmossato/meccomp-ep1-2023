# ===================== #
# Temperature equations #
# ===================== #

def orange(T, n):
    return [
        - T.h_x**2*n.a*n.b*(n.a - 1)*(T.h_y*n.b*T.cp*T.rho*n.v['value'] + T.h_y*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/(2*(n.b + 1)*(-T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*n.a**2*n.b*T.k + T.h_x**2*n.a**2*T.k + T.h_x**2*n.a*n.b*T.k - T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] - T.h_y**2*n.a*n.b**2*T.k + T.h_y**2*n.a*n.b*T.k + T.h_y**2*n.b**2*T.k - T.h_y**2*n.b*T.k)),    # j+1
        + T.h_y**2*n.b*(n.b - 1)*(T.h_x*n.a**2*T.cp*T.rho*n.u['value'] + T.h_x*n.a*T.cp*T.rho*n.u['value'] - 2*n.a*T.k + 2*T.k)/(2*(n.a + 1)*(-T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*n.a**2*n.b*T.k + T.h_x**2*n.a**2*T.k + T.h_x**2*n.a*n.b*T.k - T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] - T.h_y**2*n.a*n.b**2*T.k + T.h_y**2*n.a*n.b*T.k + T.h_y**2*n.b**2*T.k - T.h_y**2*n.b*T.k)), # i+1
        - T.h_x**2*n.a*(n.a - 1)*(T.h_y*n.b**2*T.cp*T.rho*n.v['value'] + T.h_y*n.b*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/(2*(n.b + 1)*(-T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*n.a**2*n.b*T.k + T.h_x**2*n.a**2*T.k + T.h_x**2*n.a*n.b*T.k - T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] - T.h_y**2*n.a*n.b**2*T.k + T.h_y**2*n.a*n.b*T.k + T.h_y**2*n.b**2*T.k - T.h_y**2*n.b*T.k)), # j-1
        + T.h_y**2*n.a*n.b*(n.b - 1)*(T.h_x*n.a*T.cp*T.rho*n.u['value'] + T.h_x*T.cp*T.rho*n.u['value'] - 2*n.a*T.k + 2*T.k)/(2*(n.a + 1)*(-T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*n.a**2*n.b*T.k + T.h_x**2*n.a**2*T.k + T.h_x**2*n.a*n.b*T.k - T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] - T.h_y**2*n.a*n.b**2*T.k + T.h_y**2*n.a*n.b*T.k + T.h_y**2*n.b**2*T.k - T.h_y**2*n.b*T.k)),    # i-1
        0.0,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  # indep
    ]

def black(T, n):
    return [
        0.0, # j+1
        0.0, # i+1
        0.0, # j-1
        0.0, # i-1
        0.0, # indep
    ]

def brown(T, n):
    return [
        0.0,                              # j+1
        0.0,                              # i+1
        + T.h_x**2/(T.h_x**2 + T.h_y**2), # j-1
        + T.h_y**2/(T.h_x**2 + T.h_y**2), # i-1
        0.0,                              # indep
    ]

def beige(T, n):
    return [
        + T.h_x**2/(T.h_x**2 + T.h_y**2), # j+1
        0.0,                              # i+1
        0.0,                              # j-1
        + T.h_y**2/(T.h_x**2 + T.h_y**2), # i-1
        0.0,                              # indep
    ]

def blue(T, n):
    return [
        0.0, # j+1
        0.0, # i+1
        0.0, # j-1
        0.0, # i-1
        0.0, # indep
    ]

def purple(T, n):
    return [
        + T.h_x**2*n.a*n.b*(n.a - 1)*(T.h_y*n.b*T.cp*T.rho*n.v['value'] + T.h_y*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/(2*(n.b + 1)*(T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*n.a**2*n.b*T.k - T.h_x**2*n.a**2*T.k - T.h_x**2*n.a*n.b*T.k + T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] + T.h_y**2*n.a*n.b**2*T.k - T.h_y**2*n.a*n.b*T.k - T.h_y**2*n.b**2*T.k + T.h_y**2*n.b*T.k)),    # j+1
        + T.h_y**2*n.a*n.b*(n.b - 1)*(T.h_x*n.a*T.cp*T.rho*n.u['value'] + T.h_x*T.cp*T.rho*n.u['value'] + 2*n.a*T.k - 2*T.k)/(2*(n.a + 1)*(T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*n.a**2*n.b*T.k - T.h_x**2*n.a**2*T.k - T.h_x**2*n.a*n.b*T.k + T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] + T.h_y**2*n.a*n.b**2*T.k - T.h_y**2*n.a*n.b*T.k - T.h_y**2*n.b**2*T.k + T.h_y**2*n.b*T.k)),    # i+1
        + T.h_x**2*n.a*(n.a - 1)*(T.h_y*n.b**2*T.cp*T.rho*n.v['value'] + T.h_y*n.b*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/(2*(n.b + 1)*(T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*n.a**2*n.b*T.k - T.h_x**2*n.a**2*T.k - T.h_x**2*n.a*n.b*T.k + T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] + T.h_y**2*n.a*n.b**2*T.k - T.h_y**2*n.a*n.b*T.k - T.h_y**2*n.b**2*T.k + T.h_y**2*n.b*T.k)), # j-1
        + T.h_y**2*n.b*(n.b - 1)*(T.h_x*n.a**2*T.cp*T.rho*n.u['value'] + T.h_x*n.a*T.cp*T.rho*n.u['value'] + 2*n.a*T.k - 2*T.k)/(2*(n.a + 1)*(T.h_x**2*T.h_y*n.a**2*n.b*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*n.b*T.cp*T.rho*n.v['value'] + T.h_x**2*n.a**2*n.b*T.k - T.h_x**2*n.a**2*T.k - T.h_x**2*n.a*n.b*T.k + T.h_x**2*n.a*T.k + T.h_x*T.h_y**2*n.a*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.a*n.b*T.cp*T.rho*n.u['value'] + T.h_y**2*n.a*n.b**2*T.k - T.h_y**2*n.a*n.b*T.k - T.h_y**2*n.b**2*T.k + T.h_y**2*n.b*T.k)), # i-1
        0.0,                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  # indep
    ]

def green(T, n):
    if n.v['value'] > 0: return [
        + T.h_x**2*T.k/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*T.k + 2*T.h_y**2*T.k),                                   # j+1
        0,                                                                                                                           # i+1
        + T.h_x**2*(T.h_y*T.cp*T.rho*n.v['value'] + T.k)/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*T.k + 2*T.h_y**2*T.k), # j-1
        + 2*T.h_y**2*T.k/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*T.k + 2*T.h_y**2*T.k),                                 # i-1
        0,                                                                                                                           # indep
    ]
    else: return [
        + T.h_x**2*(T.h_y*T.cp*T.rho*n.v['value'] - T.k)/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*T.k - 2*T.h_y**2*T.k), # j+1
        0,                                                                                                                           # i+1
        - T.h_x**2*T.k/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*T.k - 2*T.h_y**2*T.k),                                   # j-1
        - 2*T.h_y**2*T.k/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*T.k - 2*T.h_y**2*T.k),                                 # i-1
        0,                                                                                                                           # indep
    ]

def pink(T, n):
    if n.u['value'] > 0: return [
        0,                                                                                                                           # j+1
        + T.h_y**2*T.k/(2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k),                                   # i+1
        + 2*T.h_x**2*T.k/(2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k),                                 # j-1
        + T.h_y**2*(T.h_x*T.cp*T.rho*n.u['value'] + T.k)/(2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k), # i-1
        0,                                                                                                                           # indep
    ]
    else: return [
        0,                                                                                                                            # j+1
        + T.h_y**2*(T.h_x*T.cp*T.rho*n.u['value'] - T.k)/(-2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k), # i+1
        - 2*T.h_x**2*T.k/(-2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k),                                 # j-1
        - T.h_y**2*T.k/(-2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k),                                   # i-1
        0,                                                                                                                            # indep
    ]

def red(T, n):
    if n.u['value'] > 0: return [
        + 2*T.h_x**2*T.k/(2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k),                                 # j+1
        + T.h_y**2*T.k/(2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k),                                   # i+1
        0,                                                                                                                           # j-1
        + T.h_y**2*(T.h_x*T.cp*T.rho*n.u['value'] + T.k)/(2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k), # i-1
        0,                                                                                                                           # indep
    ]
    else: return [
        - 2*T.h_x**2*T.k/(-2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k),                                 # j+1
        + T.h_y**2*(T.h_x*T.cp*T.rho*n.u['value'] - T.k)/(-2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k), # i+1
        0,                                                                                                                            # j-1
        - T.h_y**2*T.k/(-2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k),                                   # i-1
        0,                                                                                                                            # indep
    ]

def gray(T, n):
    if n.u['value'] > 0 and n.v['value'] > 0: return [
        + T.h_x**2*T.k/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k),                                   # j+1
        + T.h_y**2*T.k/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k),                                   # i+1
        + T.h_x**2*(T.h_y*T.cp*T.rho*n.v['value'] + T.k)/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k), # j-1
        + T.h_y**2*(T.h_x*T.cp*T.rho*n.u['value'] + T.k)/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k), # i-1
        0,                                                                                                                                                                    # indep
    ]
    elif n.u['value'] > 0 and n.v['value'] < 0: return [
        - T.h_x**2*(T.h_y*T.cp*T.rho*n.v['value'] - T.k)/(-T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k), # j+1
        + T.h_y**2*T.k/(-T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k),                                   # i+1
        + T.h_x**2*T.k/(-T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k),                                   # j-1
        + T.h_y**2*(T.h_x*T.cp*T.rho*n.u['value'] + T.k)/(-T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*T.k), # i-1
        0,                                                                                                                                                                     # indep
    ]
    elif n.u['value'] < 0 and n.v['value'] > 0: return [
        - T.h_x**2*T.k/(-T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k),                                   # j+1
        + T.h_y**2*(T.h_x*T.cp*T.rho*n.u['value'] - T.k)/(-T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k), # i+1
        - T.h_x**2*(T.h_y*T.cp*T.rho*n.v['value'] + T.k)/(-T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k), # j-1
        - T.h_y**2*T.k/(-T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k),                                   # i-1
        0,                                                                                                                                                                     # indep
    ]
    else: return [
        + T.h_x**2*(T.h_y*T.cp*T.rho*n.v['value'] - T.k)/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k), # j+1
        + T.h_y**2*(T.h_x*T.cp*T.rho*n.u['value'] - T.k)/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k), # i+1
        - T.h_x**2*T.k/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k),                                   # j-1
        - T.h_y**2*T.k/(T.h_x**2*T.h_y*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*T.k),                                   # i-1
        0,                                                                                                                                                                    # indep
    ]

def cyan(T, n):
    if n.v['value'] > 0: return [
        - T.h_x**2*n.a*T.k*(n.a - 1)/(-T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.a**2*T.k + 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.a*T.k + 2*T.h_y**2*T.k),                                                                                          # j+1
        + T.h_y**2*(T.h_x*n.a**2*T.cp*T.rho*n.u['value'] + T.h_x*n.a*T.cp*T.rho*n.u['value'] - 2*n.a*T.k + 2*T.k)/((n.a + 1)*(-T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.a**2*T.k + 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.a*T.k + 2*T.h_y**2*T.k)), # i+1
        - T.h_x**2*n.a*(n.a - 1)*(T.h_y*T.cp*T.rho*n.v['value'] + T.k)/(-T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.a**2*T.k + 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.a*T.k + 2*T.h_y**2*T.k),                                                        # j-1
        + T.h_y**2*n.a*(T.h_x*n.a*T.cp*T.rho*n.u['value'] + T.h_x*T.cp*T.rho*n.u['value'] - 2*n.a*T.k + 2*T.k)/((n.a + 1)*(-T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.a**2*T.k + 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.a*T.k + 2*T.h_y**2*T.k)),    # i-1
        0,                                                                                                                                                                                                                                                                                                                                                     # indep
    ]
    else: return [
        + T.h_x**2*n.a*(n.a - 1)*(T.h_y*T.cp*T.rho*n.v['value'] - T.k)/(T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.a**2*T.k + 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.a*T.k + 2*T.h_y**2*T.k),                                                        # j+1
        + T.h_y**2*(T.h_x*n.a**2*T.cp*T.rho*n.u['value'] + T.h_x*n.a*T.cp*T.rho*n.u['value'] - 2*n.a*T.k + 2*T.k)/((n.a + 1)*(T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.a**2*T.k + 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.a*T.k + 2*T.h_y**2*T.k)), # i+1
        - T.h_x**2*n.a*T.k*(n.a - 1)/(T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.a**2*T.k + 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.a*T.k + 2*T.h_y**2*T.k),                                                                                          # j-1
        + T.h_y**2*n.a*(T.h_x*n.a*T.cp*T.rho*n.u['value'] + T.h_x*T.cp*T.rho*n.u['value'] - 2*n.a*T.k + 2*T.k)/((n.a + 1)*(T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.a**2*T.k + 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.a*T.k + 2*T.h_y**2*T.k)),    # i-1
        0,                                                                                                                                                                                                                                                                                                                                                    # indep
    ]

def yellow(T, n):
    if n.u['value'] > 0: return  [
        + T.h_x**2*n.b*(T.h_y*n.b*T.cp*T.rho*n.v['value'] + T.h_y*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/((n.b + 1)*(2*T.h_x**2*T.h_y*n.b*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.b*T.k - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.b*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.b**2*T.k - 2*T.h_y**2*n.b*T.k)),    # j+1
        + T.h_y**2*n.b*T.k*(n.b - 1)/(2*T.h_x**2*T.h_y*n.b*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.b*T.k - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.b*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.b**2*T.k - 2*T.h_y**2*n.b*T.k),                                                                                          # i+1
        + T.h_x**2*(T.h_y*n.b**2*T.cp*T.rho*n.v['value'] + T.h_y*n.b*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/((n.b + 1)*(2*T.h_x**2*T.h_y*n.b*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.b*T.k - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.b*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.b**2*T.k - 2*T.h_y**2*n.b*T.k)), # j-1
        + T.h_y**2*n.b*(n.b - 1)*(T.h_x*T.cp*T.rho*n.u['value'] + T.k)/(2*T.h_x**2*T.h_y*n.b*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.b*T.k - 2*T.h_x**2*T.k + T.h_x*T.h_y**2*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.b*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.b**2*T.k - 2*T.h_y**2*n.b*T.k),                                                        # i-1
        0,                                                                                                                                                                                                                                                                                                                                                    # indep
    ]
    else: return [
        - T.h_x**2*n.b*(T.h_y*n.b*T.cp*T.rho*n.v['value'] + T.h_y*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/((n.b + 1)*(-2*T.h_x**2*T.h_y*n.b*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.b*T.k + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.b*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.b**2*T.k + 2*T.h_y**2*n.b*T.k)),    # j+1
        + T.h_y**2*n.b*(n.b - 1)*(T.h_x*T.cp*T.rho*n.u['value'] - T.k)/(-2*T.h_x**2*T.h_y*n.b*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.b*T.k + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.b*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.b**2*T.k + 2*T.h_y**2*n.b*T.k),                                                        # i+1
        - T.h_x**2*(T.h_y*n.b**2*T.cp*T.rho*n.v['value'] + T.h_y*n.b*T.cp*T.rho*n.v['value'] + 2*n.b*T.k - 2*T.k)/((n.b + 1)*(-2*T.h_x**2*T.h_y*n.b*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.b*T.k + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.b*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.b**2*T.k + 2*T.h_y**2*n.b*T.k)), # j-1
        - T.h_y**2*n.b*T.k*(n.b - 1)/(-2*T.h_x**2*T.h_y*n.b*T.cp*T.rho*n.v['value'] - 2*T.h_x**2*n.b*T.k + 2*T.h_x**2*T.k + T.h_x*T.h_y**2*n.b**2*T.cp*T.rho*n.u['value'] - T.h_x*T.h_y**2*n.b*T.cp*T.rho*n.u['value'] - 2*T.h_y**2*n.b**2*T.k + 2*T.h_y**2*n.b*T.k),                                                                                          # i-1
        0,                                                                                                                                                                                                                                                                                                                                                     # indep
    ]

def light_blue(T, n):
    if n.v['value'] > 0: return [
        + T.h_x**2*n.a*T.k*(n.a - 1)/(T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.a**2*T.k - 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.a*T.k - 2*T.h_y**2*T.k),                                                                                          # j+1
        + T.h_y**2*n.a*(T.h_x*n.a*T.cp*T.rho*n.u['value'] + T.h_x*T.cp*T.rho*n.u['value'] + 2*n.a*T.k - 2*T.k)/((n.a + 1)*(T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.a**2*T.k - 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.a*T.k - 2*T.h_y**2*T.k)),    # i+1
        + T.h_x**2*n.a*(n.a - 1)*(T.h_y*T.cp*T.rho*n.v['value'] + T.k)/(T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.a**2*T.k - 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.a*T.k - 2*T.h_y**2*T.k),                                                        # j-1
        + T.h_y**2*(T.h_x*n.a**2*T.cp*T.rho*n.u['value'] + T.h_x*n.a*T.cp*T.rho*n.u['value'] + 2*n.a*T.k - 2*T.k)/((n.a + 1)*(T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] - T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.a**2*T.k - 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.a*T.k - 2*T.h_y**2*T.k)), # i-1
        0,                                                                                                                                                                                                                                                                                                                                                    # indep
    ]
    else: return [
        - T.h_x**2*n.a*(n.a - 1)*(T.h_y*T.cp*T.rho*n.v['value'] - T.k)/(-T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.a**2*T.k - 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.a*T.k - 2*T.h_y**2*T.k),                                                        # j+1
        + T.h_y**2*n.a*(T.h_x*n.a*T.cp*T.rho*n.u['value'] + T.h_x*T.cp*T.rho*n.u['value'] + 2*n.a*T.k - 2*T.k)/((n.a + 1)*(-T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.a**2*T.k - 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.a*T.k - 2*T.h_y**2*T.k)),    # i+1
        + T.h_x**2*n.a*T.k*(n.a - 1)/(-T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.a**2*T.k - 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.a*T.k - 2*T.h_y**2*T.k),                                                                                          # j-1
        + T.h_y**2*(T.h_x*n.a**2*T.cp*T.rho*n.u['value'] + T.h_x*n.a*T.cp*T.rho*n.u['value'] + 2*n.a*T.k - 2*T.k)/((n.a + 1)*(-T.h_x**2*T.h_y*n.a**2*T.cp*T.rho*n.v['value'] + T.h_x**2*T.h_y*n.a*T.cp*T.rho*n.v['value'] + 2*T.h_x**2*n.a**2*T.k - 2*T.h_x**2*n.a*T.k + 2*T.h_x*T.h_y**2*n.a*T.cp*T.rho*n.u['value'] + 2*T.h_y**2*n.a*T.k - 2*T.h_y**2*T.k)), # i-1
        0,                                                                                                                                                                                                                                                                                                                                                     # indep
    ]
