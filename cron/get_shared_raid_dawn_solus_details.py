#!/usr/bin/env python

# Get raid details for table/serverid

import yaml
import re
import json
import requests
import MySQLdb as mdb

from datetime import datetime

config = yaml.load(open('../private/apikey').read())

base = 'http://ugup.5thplanetgames.com/api/'

conn = mdb.connect(host=config['dbhost'],
                   user=config['dbuser'],
                   passwd=config['dbpass'],
                   db=config['db'],
                   charset='utf8',
                   use_unicode=True)

bosses_dict = {}

summoner_cache = {}

cursor = conn.cursor()

def str2bool(s):
    if str(s).lower() in ("yes", "true", "t", "1"):
        return 1
    else:
        return 0


def build_dictionaries():
    dawn_query = ("SELECT name, postimage FROM dawn_raids")
    cursor.execute(dawn_query)
    for (name, postimage) in cursor:
        if len(name) and len(postimage):
            bosses_dict[postimage] = name

    suns_query = ("SELECT shortname, postimage FROM suns_raids")
    cursor.execute(suns_query)
    for (shortname, postimage) in cursor:
        if len(shortname) and len(postimage):
            bosses_dict[postimage] = shortname

    if not bosses_dict.has_key('war_damned_shade'):
        bosses_dict['war_damned_shade'] = "War Damned Shade"


def set_raid_info():
    raid_info = {
        'currenthealth': 0,
        'enragehealth': 0,
        'maxhealth': 0,
        'debuff1id': 0,
        'debuff2id': 0,
        'debuff3id': 0,
        'debuff4id': 0,
        'debuff5id': 0,
        'debuff6id': 0,
        'iscomplete': 0,
        'nummembers': 0,
        'summonerid': '',
        'summoner_fname': '',
        'summoner_guildID': 0,
        'summoner_level': 0,
        'summoner_platform': 0,
        'summoner_ugupoptout': 0,
        'maxattackers': 0,
    }
    return raid_info


def set_summoner_info():
    summoner_info = {
        'summoner_fname': '',
        'summoner_guildID': 0,
        'summoner_level': 0,
        'summoner_platform': 0,
        'summoner_ugupoptout': 0,
    }
    return summoner_info


def get_var(var, type):
    v = var.split("'")
    if type == "str":
        return str(v[1])
    if type == "int":
        return int(v[1])


def get_raid_info_url(raid_id, raid_hash, platform, game, serverid=None):
    # http://ugup.5thplanetgames.com/api/raid/hash/${RAID_ID}/${HASH}?apikey=${API_KEY}&platform=${PLATFORM}&game=${GAME}
    if serverid is None:
        serverid = 1
    api_url = base + "raid/hash/" + str(raid_id) + "/" + str(raid_hash) \
           + "?apikey=" + config["apikey"] \
           + "&platform=" + str(platform) \
           + "&game=" + str(game) \
           + "&serverid=" + str(serverid)
    return api_url


def get_raid_details(raid_url, raid_info):
    request = requests.get(raid_url)
    if not request.status_code == 200:
        request.raise_for_status()
    else:
        data = json.loads(request.text)
        for item, val in data['result'].iteritems():
            # If it's a nested json result, then it loops through?
            if item not in ('definition', 'hash'):
                if item == 'iscomplete':
                    raid_info[str(item)] = int(str2bool(val))
                elif item == 'summonerid':
                    raid_info[str(item)] = str(val.strip())
                else:
                    raid_info[str(item)] = int(val)
            if item in ('definition'):
                for s, v in data['result']['definition'].iteritems():
                    if s == 'maxattackers':
                        raid_info[str(s)] = int(v)


def ugup_request(table, game, serverid=None, platform='facebook'):
    if serverid is None:
        serverid = 1

    sql_query = ("SELECT id, platform, raid_id, raid_hash, serverid FROM %s WHERE serverid=%s AND iscomplete is NULL OR iscomplete!=1;" % ( table, serverid))

    cursor.execute(sql_query)

    for (id, platform, raid_id, raid_hash, serverid) in cursor:
        if config["verbose_mode"]:
            print 'Table: '+ table + ': Raid ID: ' + str(id)

        raid_info = set_raid_info()
        get_raid_details(get_raid_info_url(raid_id, raid_hash, platform, game, serverid), raid_info)

        # summoner_info = set_summoner_info()

        #
        update_time = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

        sql = "UPDATE %s SET update_time='%s', currenthealth='%s', enragehealth='%s', maxhealth='%s', debuff1id='%s', \
               debuff2id='%s', debuff3id='%s', debuff4id='%s', debuff5id='%s', debuff6id='%s', iscomplete='%s', \
               nummembers='%s', maxattackers='%s', summonerid='%s' WHERE id='%s';" \
              % ( table, update_time, raid_info['currenthealth'], raid_info['enragehealth'], raid_info['maxhealth'],
                  raid_info['debuff1id'], raid_info['debuff2id'], raid_info['debuff3id'],
                  raid_info['debuff4id'], raid_info['debuff5id'], raid_info['debuff6id'],
                  raid_info['iscomplete'], raid_info['nummembers'], raid_info['maxattackers'], raid_info['summonerid'],
                  id
                 )

        cursor.execute(sql)
        conn.commit()

# main

build_dictionaries()

ugup_request('dawn_shared_raids', 'dawn')

cursor.close()
conn.close()

if config["verbose_mode"]:
    print "Job's Done!"