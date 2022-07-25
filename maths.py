def sign(x):
    return 1 if x > 0 else (0 if x == 0 else -1)

def floor(x):
    return x // 1

def newtons_method(f, guess):
    def improve_guess(g):
        h = 0.0000001
        return guess - f(guess)*h/(f(guess+h) - f(g))
    while f(guess) > 0.00000001:
        guess = improve_guess(guess)
    return guess

def sqrt(x):
    return newtons_method((lambda z: z * z - x), x / 2)

def length(a):
    sum = 0
    for i in range(len(a)):
        sum += a[i] * a[i]
    return sqrt(sum)

def distance(a, b):
    c = []
    for i in range(len(a)):
        c.append(a[i] - b[i])
    return length(c)

def normalize(dir):
    if dir == (0, 0):
        return (0, 0)
    else:
        (x, y) = dir
        l = length(dir)
        return (x/l, y/l)

def lerp_pos(from_pos, to_pos, t):
    (from_x, from_y) = from_pos
    (to_x, to_y) = to_pos
    return (from_x + (to_x - from_x)*t, from_y + (to_y - from_y)*t)