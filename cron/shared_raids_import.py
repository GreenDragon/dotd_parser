#!/usr/bin/env python

# Import all tables from ugup that have proc_name mappings

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


def shared_api_call_path(item, platform, game, serverid=None):
    # http://ugup.5thplanetgames.com/api/${ITEM}/shared?apikey=${API_KEY}&platform=${PLATFORM}&game=${GAME}
    if serverid is None:
        serverid = 1
    path = base + item + "/shared?apikey=" + config["apikey"] \
           + "&platform=" + platform \
           + "&game=" + game \
           + "&serverid=" + str(serverid)
    return path


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


def get_raid_info(raid_url, raid_info_dict):
    request = requests.get(raid_url)
    if not request.status_code == 200:
        request.raise_for_status()
    else:
        data = json.loads(request.text)
        for item, val in data['result'].iteritems():
            # If it's a nested json result, then it loops through? I guess... I don't know... this works
            if item not in ('definition', 'hash'):
                if item == 'iscomplete':
                    raid_info_dict[str(item)] = int(str2bool(val))
                elif item == 'summonerid':
                    raid_info_dict[str(item)] = str(val.strip())
                else:
                    raid_info_dict[str(item)] = int(val)
            if item in ('definition'):
                for s, v in data['result']['definition'].iteritems():
                    if s == 'maxattackers':
                        raid_info_dict[str(s)] = int(v)


def get_profile_url(profile_id, platform, game, serverid=None):
    # http://ugup.5thplanetgames.com/api/profile/${PROFILE}?apikey=${API_KEY}&platform=${PLATFORM}&game=${GAME}
    if serverid is None:
        serverid = 1
    url = base + "profile/" + str(profile_id) \
           + "?apikey=" + config["apikey"] \
           + "&platform=" + str(platform) \
           + "&game=" + str(game) \
           + "&serverid=" + str(serverid)
    return url


def store_summoner_cache(platform, game, serverid, summoner_id, summoner_info):
    check = str(platform) + ":" + str(game) + ":" + str(serverid) + ":" + str(summoner_id)
    if not summoner_cache.has_key(check):
        summoner_cache[check] = summoner_info


def get_summoner_cache(platform, game, serverid, summoner_id, summoner_info):
    check = str(platform) + ":" + str(game) + ":" + str(serverid) + ":" + str(summoner_id)
    if summoner_cache.has_key(check):
        summoner_info = {}
        summoner_info = summoner_cache[check]


def get_summoner_info(summoner_id, platform, game, serverid, summoner_info):
    get_summoner_cache(platform, game, serverid, summoner_id, summoner_info)
    if summoner_info['summoner_fname'] != '':
        return
    request = requests.get(get_profile_url(summoner_id, platform, game, serverid))
    if not request.status_code == 200:
        request.raise_for_status()
    else:
        data = json.loads(request.text)
        if data.has_key('result'):
            for item, val in data['result'].iteritems():
                if item in ('level', 'guildID', 'ugupoptout', 'platform', 'fname'):
                    sname = "summoner_" + str(item)
                    if item == 'fname':
                        summoner_info[sname] = str(val.strip())
                    else:
                        summoner_info[sname] = int(val)
        else:
            # User opted out
            summoner_info['summoner_ugupoptout'] = 1
            fname = "opted_out: " + str(summoner_id)
            summoner_info['summoner_fname'] = fname
        #if summoner_info['summoner_ugupoptout'] == 0:
        store_summoner_cache(platform, game, serverid, summoner_id, summoner_info)


def get_var(var, type):
    v = var.split("'")
    if type == "str":
        return str(v[1])
    if type == "int":
        return int(v[1])


def ugup_request(path, table, game, platform='facebook'):
    request = requests.get(path)
    if not request.status_code == 200:
        request.raise_for_status()
    else:
        data = json.loads(request.text)
        for item in data['result']:
            if config["verbose_mode"]:
                print 'Table: '+ table + ': Raid ID: ' + str(item['id'])

            # These json/hash fields should always be constant in all cases
            id = int(item['id'])
            create_time = str(item['create_time'].strip())
            link = str(item['link'].strip())
            update_time = str(datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

            link_name = ''
            raid_id = -1
            difficulty = -1
            raid_boss = ''
            raid_hash = ''
            serverid = -1

            link = re.sub('[<>]', '', link)
            links = link.split()

            for line in links:
                if "raidhelp" in line:
                    link_name = str(line)
                if "raid_id=" in line:
                    raid_id = get_var(line, "int")
                if "difficulty=" in line:
                    difficulty = get_var(line, "int")
                if "raid_boss=" in line:
                    raid_boss = get_var(line, "str")
                    if bosses_dict.has_key(raid_boss):
                        raid_boss = re.escape(str(bosses_dict[raid_boss]))
                if "hash=" in line:
                    raid_hash = get_var(line, "str")
                if "serverid=" in line:
                    serverid = get_var(line, "int")

            # LoTS doesn't seem to have multiple servers...
            if serverid == -1:
                serverid = 1

            raid_info = { 'currenthealth': 0,
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

            get_raid_info(get_raid_info_url(raid_id, raid_hash, platform, game, serverid), raid_info)

            summoner_info = { 'summoner_fname': '',
                              'summoner_guildID': 0,
                              'summoner_level': 0,
                              'summoner_platform': 0,
                              'summoner_ugupoptout': 0,
                            }

            get_summoner_info(raid_info['summonerid'], platform, game, serverid, summoner_info)

            if table in ['dawn_shared_raids', 'suns_shared_raids']:
                sql = "INSERT INTO %s ( id, create_time, update_time, platform, link_name, raid_id, difficulty, \
                    raid_boss, raid_hash, serverid, currenthealth, enragehealth, maxhealth, debuff1id, debuff2id, \
                    debuff3id, debuff4id, debuff5id, debuff6id, iscomplete, nummembers, maxattackers, summonerid, \
                    summoner_fname, summoner_guildID, summoner_level, summoner_platform, summoner_ugupoptout ) \
                    VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                    '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ) \
                    ON DUPLICATE KEY UPDATE update_time='%s', platform='%s', link_name='%s', raid_id='%s', \
                    difficulty='%s', raid_boss='%s', raid_hash='%s', serverid='%s', currenthealth='%s', \
                    enragehealth='%s', maxhealth='%s', debuff1id='%s', debuff2id='%s', debuff3id='%s', debuff4id='%s', \
                    debuff5id='%s', debuff6id='%s', iscomplete='%s', nummembers='%s', maxattackers='%s', \
                    summonerid='%s', summoner_fname='%s', summoner_guildID='%s', summoner_level='%s', \
                    summoner_platform='%s', summoner_ugupoptout='%s';" \
                    % (table,
                       id, create_time, update_time, platform, link_name, raid_id, difficulty, raid_boss, raid_hash,
                       serverid, raid_info['currenthealth'], raid_info['enragehealth'], raid_info['maxhealth'],
                       raid_info['debuff1id'], raid_info['debuff2id'], raid_info['debuff3id'], raid_info['debuff4id'],
                       raid_info['debuff5id'], raid_info['debuff6id'], raid_info['iscomplete'],
                       raid_info['nummembers'], raid_info['maxattackers'], raid_info['summonerid'],
                       summoner_info['summoner_fname'], summoner_info['summoner_guildID'],
                       summoner_info['summoner_level'], summoner_info['summoner_platform'],
                       summoner_info['summoner_ugupoptout'],
                       update_time, platform, link_name, raid_id, difficulty, raid_boss, raid_hash, serverid,
                       raid_info['currenthealth'], raid_info['enragehealth'], raid_info['maxhealth'],
                       raid_info['debuff1id'], raid_info['debuff2id'], raid_info['debuff3id'], raid_info['debuff4id'],
                       raid_info['debuff5id'], raid_info['debuff6id'], raid_info['iscomplete'],
                       raid_info['nummembers'], raid_info['maxattackers'], raid_info['summonerid'],
                       summoner_info['summoner_fname'], summoner_info['summoner_guildID'],
                       summoner_info['summoner_level'], summoner_info['summoner_platform'],
                       summoner_info['summoner_ugupoptout']
                      )

                cursor.execute(sql)
                conn.commit()

# main

build_dictionaries()

ugup_request(shared_api_call_path('raid', 'facebook', 'dawn'), 'dawn_shared_raids', 'dawn')
ugup_request(shared_api_call_path('raid', 'facebook', 'dawn', 2), 'dawn_shared_raids', 'dawn')
ugup_request(shared_api_call_path('raid', 'facebook', 'suns'), 'suns_shared_raids', 'suns')

cursor.close()
conn.close()

print "Job's Done!"
