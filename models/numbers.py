from __future__ import division

def percentage(x, y):
    if y == 0:
        return "Divide/0 Error"
    else:
        percentage = (float(x) / y) * 100
    return format(percentage, ',.3f')


def commify(x):
    if type(x) in [ type(0), type(0L) ]:
        return format(x, ',d')
    elif type(x) in [ type(0.0) ]:
        return format(x, ',.2f')
    else:
        return x
