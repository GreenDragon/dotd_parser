from __future__ import division
from string import digits
import urllib

def percentage(x, y):
    if y == 0:
        return "Divide/0 Error"
    else:
        return commify( (float(x) / y) * 100)


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


def safe_divide(x, y):
    if y == 0:
        return "Divide/0 Error"
    else:
        return commify( (float(x) / y) )


def gen_wiki_url(proc_name, suns_mode):
    dotd_wiki = 'http://dotd.wikia.com/wiki/Special:Search?search='
    lots_wiki = 'http://zoywiki.com/index.php?search=LotS+'
    if suns_mode:
        return lots_wiki + str(urllib.quote_plus(proc_name)) + '&button=&title=Special%3ASearch'
    else:
        return dotd_wiki + str(urllib.quote_plus(proc_name)) + '&fulltext=Search'
