#!/usr/bin/env python

# Import all tables from ugup that have proc_name mappings

import yaml
import re
import json
import requests
import MySQLdb as mdb

config = yaml.load(open('../private/apikey').read())

base = 'http://ugup.5thplanetgames.com/api/'

conn = mdb.connect(host=config['dbhost'],
                   user=config['dbuser'],
                   passwd=config['dbpass'],
                   db=config['db'],
                   charset='utf8',
                   use_unicode=True)

bosses_dict = {}

cursor = conn.cursor()

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
    if serverid is None:
        serverid = 1
    path = base + item + "/shared?apikey=" + config["apikey"] \
           + "&platform=" + platform + "&game=" + game \
           + "&serverid=" + str(serverid)
    return path

def get_var(var, type):
    v = var.split("'")
    if type == "str":
        return str(v[1])
    if type == "int":
        return int(v[1])

def ugup_request(path, table, platform='facebook'):
    request = requests.get(path)
    if not request.status_code == 200:
        request.raise_for_status()
    else:
        data = json.loads(request.text)
        for item in data['result']:
            if config["verbose_mode"]:
                print table + ': Raid ID: ' + str(item['id'])

            # These json/hash fields should always be constant in all cases

            id = int(item['id'])
            create_time = str(item['create_time'].strip())
            link = str(item['link'].strip())

            link_name = ''
            raid_id = -1
            difficulty = -1
            raid_boss = ''
            raid_hash = ''
            serverid = -1

            link = re.sub('[<>]', '', link)
            links = link.split()
            print ""
            for line in links:
                if "raidhelp" in line:
                    link_name = str(line)
                if "raid_id=" in line:
                    raid_id = get_var(line, "int")
                if "difficulty=" in line:
                    difficulty = get_var(line, "int")
                if "raid_boss=" in line:
                    raid_boss = get_var(line, "str")
                    #print "Working on raid_boss: " + str(raid_boss)
                    if bosses_dict.has_key(raid_boss):
                        #print "Found: " + str(bosses_dict[raid_boss])
                        raid_boss = re.escape(str(bosses_dict[raid_boss]))
                if "hash=" in line:
                    raid_hash = get_var(line, "str")
                if "serverid=" in line:
                    serverid = get_var(line, "int")

            # LoTS doesn't seem to have multiple servers...
            if serverid == -1:
                serverid = 1

            if table in ['dawn_shared_raids', 'suns_shared_raids']:
                sql = "INSERT INTO %s ( id, create_time, platform, link_name, raid_id, difficulty, raid_boss, \
                    raid_hash, serverid ) \
                    VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') \
                    ON DUPLICATE KEY UPDATE create_time='%s', platform='%s', link_name='%s', raid_id='%s', \
                    difficulty='%s', raid_boss='%s', raid_hash='%s', serverid='%s';" \
                    % (table, id, create_time, platform, link_name, raid_id, difficulty, raid_boss, raid_hash,
                       serverid, create_time, platform, link_name, raid_id, difficulty, raid_boss, raid_hash,
                       serverid)

                cursor.execute(sql)

    conn.commit()

# main

build_dictionaries()

# print bosses_dict

ugup_request(shared_api_call_path('raid', 'facebook', 'dawn'), 'dawn_shared_raids')
ugup_request(shared_api_call_path('raid', 'facebook', 'dawn', 2), 'dawn_shared_raids')
ugup_request(shared_api_call_path('raid', 'facebook', 'suns'), 'suns_shared_raids')


cursor.close()
conn.close()

print "Job's Done!"
