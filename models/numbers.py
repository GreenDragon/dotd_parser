from __future__ import division
from string import digits
import urllib


def percentage(x, y):
    if y == 0:
        return "Divide/0 Error"
    else:
        return commify((float(x)/y) * 100)


def commify(x):
    if type(x) in [ type(0), type(0L) ]:
        return format(x, ',d')
    elif type(x) in [ type(0.0) ]:
        return format(x, ',.2f')
    else:
        return x


def isnum(s):
    if s.translate(None, digits).translate(None, ','):
        return False
    else:
        return True


def safe_divide(x, y, precision=2):
    if y == 0:
        return "0"
    else:
        if precision == 0:
            return commify(int(round((float(x)/y), precision)))
        else:
            return commify(round((float(x)/y), precision))


def safe_divide_no_format(x, y):
    if y == 0:
        return 0
    else:
        return float(x) / float(y)


def gen_wiki_url(proc_name, suns_mode):
    dotd_wiki = 'http://dotd.wikia.com/wiki/Special:Search?search='
    lots_wiki = 'http://zoywiki.com/index.php?search=LotS+'
    if suns_mode:
        return lots_wiki + str(urllib.quote_plus(proc_name)) + '&button=&title=Special%3ASearch'
    else:
        return dotd_wiki + str(urllib.quote_plus(proc_name)) + '&fulltext=Search'
