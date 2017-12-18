def int2base(x, base):
    digits = []
    if x < 0:
        sign = -1
    elif x == 0:
        return "0"
    else:
        sign = 1
    x = sign * x
    while x:
        digits.append(int(x % base))
        x /= base
    digits.reverse()
    return ','.join([str(i) for i in digits])