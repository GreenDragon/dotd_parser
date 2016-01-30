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


def magify_array(dbf1, dbf2, dbf3, dbf4, dbf5, dbf6 ):
    s = []
    for var in (dbf1, dbf2, dbf3, dbf4, dbf5, dbf6):
        if int(var) != 0:
            s.append(int(var))
    return sorted(s)


def gen_magics_url(row, magic_map):
    u1 = '<a href="#" title="'
    # magic_map[row.debuff1id]['name']
    u2 = '"><img src="https://5thplanetdawn.insnw.net/dotd_live/images/items/magic/'
    # magic_map[row.debuff1id]['img_url']
    u3 = '" style="width: 24px; height: 24px"></a>'
    sorted_a = []
    sorted_a = magify_array(row.debuff1id,row.debuff2id,row.debuff3id,row.debuff4id,row.debuff5id,row.debuff6id)
    img_urls = ''
    for x in sorted_a:
        if magic_map.has_key(x):
            img_urls += u1 + str(magic_map[x]['name']) + u2 + str(magic_map[x]['img_url']) + u3 + ' '
    if len(img_urls):
        return img_urls


def gen_tactics_url(row, tactics_map):
    u1 = '<a href="#" title="'
    # tactics_map[row.debuff1id]['name']
    u2 = '"><img src="https://5thplanetdawn.insnw.net/lots_live/images/items/magic/'
    # tactics_map[row.debuff1id]['img_url']
    u3 = '" style="width: 24px; height: 24px"></a>'
    sorted_a = []
    sorted_a = magify_array(row.debuff1id,row.debuff2id,row.debuff3id,row.debuff4id,row.debuff5id,row.debuff6id)
    img_urls = ''
    for x in sorted_a:
        if tactics_map.has_key(x):
            img_urls += u1 + str(tactics_map[x]['name']) + u2 + str(tactics_map[x]['img_url']) + u3 + ' '
    if len(img_urls):
        return img_urls


def difficultize(difficulty):
    if difficulty == 1:
        return "Normal"
    elif difficulty == 2:
        return "Hard"
    elif difficulty == 3:
        return "Legendary"
    elif difficulty == 4:
        return "Nightmare"
    else:
        return difficulty


def gen_facebook_dotd_raid_url(link_name, raid_id, difficulty, raid_boss, raid_hash, serverid):
    return "https://apps.facebook.com/dawnofthedragons/?action_type=" + link_name \
           + "&raid_id=" + str(raid_id) \
           + "&difficulty=" + str(difficulty) \
           + "&raid_boss=" + str(raid_boss) \
           + "&hash=" + str(raid_hash) \
           + "&serverid=" + str(serverid)


def gen_facebook_lots_raid_url(link_name, raid_id, difficulty, raid_boss, raid_hash):
    return "https://apps.facebook.com/legacythousandsuns/?action_type=" + link_name \
           + "&raid_id=" + str(raid_id) \
           + "&difficulty=" + str(difficulty) \
           + "&raid_boss=" + str(raid_boss) \
           + "&hash=" + str(raid_hash)
