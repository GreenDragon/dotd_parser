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
        if x in magic_map:
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
        if x in tactics_map:
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


# armor
# facebook
# kongregate
# newgrounds
def get_platform_server_name(platform, serverid):
    p = str(platform).capitalize()
    if platform == 'armor':
        if serverid == 1:
            return p + " Roland"
        else:
            return p + " Kasan (World)"
    elif platform == 'facebook':
        if serverid == 1:
            return p + " Solus"
        else:
            return p + " Kasan (World)"
    elif platform == 'kongregate':
        if serverid == 1:
            return p + " Elyssa"
        else:
            return p + " Kasan (World)"
    elif platform == 'newgrounds':
        if serverid == 1:
            return p + " Roland"
        else:
            return p + " Kasan (World)"
    else:
        return "Wicked!"


def gen_dotd_raid_url(link_name, raid_id, difficulty, raid_boss, raid_hash, platform, serverid):
    if platform == 'armor':
        return "https://armorgames.com/dawn-of-the-dragons-game/13509?ar_action_type=" + link_name \
            + "&ar_raid_id=" + str(raid_id) \
            + "&ar_difficulty=" + str(difficulty) \
            + "&ar_raid_boss=" + str(raid_boss) \
            + "&ar_hash=" + str(raid_hash) \
            + "&ar_serverid=" + str(serverid)
    elif platform == 'facebook':
        return "https://apps.facebook.com/dawnofthedragons/?action_type=" + link_name \
            + "&raid_id=" + str(raid_id) \
            + "&difficulty=" + str(difficulty) \
            + "&raid_boss=" + str(raid_boss) \
            + "&hash=" + str(raid_hash) \
            + "&serverid=" + str(serverid)
    elif platform == 'kongregate':
        return "https://www.kongregate.com/games/5thPlanetGames/dawn-of-the-dragons?kv_action_type=" + link_name \
            + "&kv_raid_id=" + str(raid_id) \
            + "&kv_difficulty=" + str(difficulty) \
            + "&kv_raid_boss=" + str(raid_boss) \
            + "&kv_hash=" + str(raid_hash) \
            + "&kv_serverid=" + str(serverid)
    elif platform == 'newgrounds':
        return "https://newgrounds.com/portal/view/609826?ng_action_type=" + link_name \
            + "&ng_raid_id=" + str(raid_id) \
            + "&ng_difficulty=" + str(difficulty) \
            + "&ng_raid_boss=" + str(raid_boss) \
            + "&ng_hash=" + str(raid_hash) \
            + "&ng_serverid=" + str(serverid)
    else:
        return "https://localhost/bad_platform"


def gen_lots_raid_url(link_name, raid_id, difficulty, raid_boss, raid_hash, platform):
    # std maps to all servers?
    # http://www.legacyofathousandsuns.com/game/?action_type=raidhelp&raid_id=19327366&hash=2175qs6irx
    #
    # ar_action_type=raidhelp&ar_raid_id=19327289&ar_hash=654c24v6YK
    # https://armorgames.com/legacy-of-a-thousand-suns-game/13510?ar_action_type=raidhelp&ar_raid_id=19327365&ar_hash=02Z8WkMpF6
    if platform == 'armor':
        return "https://armorgames.com/legacy-of-a-thousand-suns-game/13510?ar_action_type=" + link_name \
            + "&ar_raid_id=" + str(raid_id) \
            + "&ar_hash=" + str(raid_hash)
            # + "&ar_difficulty=" + str(difficulty) \
            # + "&ar_raid_boss=" + str(raid_boss) \
            # + "&ar_hash=" + str(raid_hash)
    # action_type=raidhelp&raid_id=19327331&hash=0sb9CtpHEo
    # https://apps.facebook.com/legacythousandsuns/?action_type=raidhelp&raid_id=19327369&hash=wnzMd8kxeb
    elif platform == 'facebook':
        return "https://apps.facebook.com/legacythousandsuns/?action_type=" + link_name \
           + "&raid_id=" + str(raid_id) \
           + "&hash=" + str(raid_hash)
           # + "&difficulty=" + str(difficulty) \
           # + "&raid_boss=" + str(raid_boss) \
           # + "&hash=" + str(raid_hash)
    # kv_action_type=raidhelp&kv_raid_id=19327289&kv_hash=654c24v6YK
    # https://www.kongregate.com/games/5thplanetgames/legacy-of-a-thousand-suns?kv_action_type=raidhelp&kv_raid_id=19327365&kv_hash=02Z8WkMpF6
    elif platform == 'kongregate':
        return "https://www.kongregate.com/games/5thplanetgames/legacy-of-a-thousand-suns?kv_action_type=" + link_name \
            + "&kv_raid_id=" + str(raid_id) \
            + "&kv_hash=" + str(raid_hash)
            # + "&kv_difficulty=" + str(difficulty) \
            # + "&kv_raid_boss=" + str(raid_boss) \
            # + "&kv_hash=" + str(raid_hash)
    # ng_action_type=raidhelp&ng_raid_id=19327331&ng_hash=0sb9CtpHEo
    # https://www.newgrounds.com/portal/view/608877?ng_action_type=raidhelp&ng_raid_id=19327389&ng_hash=Y9CGQI6hzf
    elif platform == 'newgrounds':
        return "https://www.newgrounds.com/portal/view/608877?ng_action_type=" + link_name \
            + "&ng_raid_id=" + str(raid_id) \
            + "&ng_hash=" + str(raid_hash)
            # + "&ng_difficulty=" + str(difficulty) \
            # + "&ng_raid_boss=" + str(raid_boss) \
            # + "&ng_hash=" + str(raid_hash)
    else:
        return "https://localhost/bad_platform"


def gen_short_raid_link(raid_id, raid_hash):
    return "http://127.0.0.1/?raid_id=" + str(raid_id) + "&hash=" + str(raid_hash)
