from __future__ import division

def percentage(x, y):
    if y == 0:
        return
    else:
        percentage = (float(x) / y) * 100
    return percentage


def number_format(x):
    # return locale.format('%d', num, grouping=True)
    if type(x) not in [type(0), type(0L)]:
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + intWithCommas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = ",%03d%s" % (r, result)
    return "%d%s" % (x, result)


def rounding(num):
    return format(num, '.2f')
