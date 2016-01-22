import urllib

def gen_wiki_url(proc_name, suns_mode):
    dotd_wiki = 'http://dotd.wikia.com/wiki/Special:Search?search='
    lots_wiki = 'http://zoywiki.com/index.php?search=LotS+'
    if suns_mode:
        return lots_wiki + str(urllib.quote_plus(proc_name)) + '&button=&title=Special%3ASearch'
    else:
        return dotd_wiki + str(urllib.quote_plus(proc_name)) + '&fulltext=Search'


def monify(suns_mode):
    if suns_mode:
        return "Credits"
    else:
        return "Gold"


def magify(suns_mode):
    if suns_mode:
        return "Tactics"
    else:
        return "Magics"


def magify_title(suns_mode):
    if suns_mode:
        return "Tactic"
    else:
        return "Magic"


def magify_modes(suns_mode):
    if suns_mode:
        return "applied/removed"
    else:
        return "cast/dispelled"
