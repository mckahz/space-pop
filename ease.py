def in_power(p):
    return (lambda x: x**p)

def out_power(p):
    return (lambda x: 1 - (abs(1-x))**p)

def in_out_power(p):
    return in_out(in_power(p), out_power(p))

def in_quad(x):
    return x * x

def out_quad(x):
    return 1 - (x - 1) * (x - 1)

def in_out(ease_in, ease_out):
    return (lambda x: ease_in(x*2) / 2 if x < 0.5 else (ease_out((x-0.5)*2) + 1) /2)

def in_out_quad(x):
    return in_out(in_quad, out_quad)(x)

def invert(x):
    return 1 - x

def linear(x):
    return x

def in_cube(x):
    return x * x * x

def out_cube(x):
    return 1 + (x - 1) * (x - 1) * (x - 1)

def in_out_cube(x):
    return in_out(in_cube, out_cube)(x)

def in_quart(x):
    return x * x * x * x

def out_quart(x):
    return 1 - (x - 1) * (x - 1) * (x - 1) * (x - 1)

def in_out_quart(x):
    return in_out(in_quart, out_quart)(x)

def out_quad_snap(x):
    middle_point = 0.8
    apex = 1.02
    snap = 4
    if x < middle_point:
        return apex * out_quad(x/middle_point)
    else:
        return - ((apex-1)/((1-middle_point)**snap)) * (x - middle_point)**snap + apex