#!/usr/bin/env python

# Grab all actively shared raids

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

cursor = conn.cursor()

def build_dictionaries():
    dawn_query = ("SELECT shortname, postimage FROM dawn_raids ORDER by postimage ASC, maxattackers DESC")
    cursor.execute(dawn_query)
    for (shortname, postimage) in cursor:
        if len(shortname) and len(postimage):
            bosses_dict[postimage] = shortname

    suns_query = ("SELECT shortname, postimage FROM suns_raids")
    cursor.execute(suns_query)
    for (shortname, postimage) in cursor:
        if len(shortname) and len(postimage):
            bosses_dict[postimage] = shortname

    if 'war_damned_shade' not in bosses_dict:
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


def get_link_details(link):
    link_name = ''
    raid_id = -1
    difficulty = -1
    raid_boss = ''
    raid_boss_human = ''
    raid_hash = ''
    # LoTS doesn't seem to have multiple servers...
    serverid = 1

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
            if raid_boss in bosses_dict:
                raid_boss_human = re.escape(str(bosses_dict[raid_boss]))
            else:
                raid_boss_human = raid_boss
        if "hash=" in line:
            raid_hash = get_var(line, "str")
        if "serverid=" in line:
            serverid = get_var(line, "int")
    return link_name, raid_id, difficulty, raid_boss, raid_boss_human, raid_hash, serverid


def get_var(var, type):
    v = var.split("'")
    if type == "str":
        return str(v[1])
    if type == "int":
        try:
            return int(v[1])
        except ValueError:
            i = re.findall(r'\d+', v[1])
            return int(i[0])

def ugup_request(path, table, platform):
    try:
        request = requests.get(path)
    except requests.exceptions.HTTPError, e:
        if config["verbose_mode"]:
            print "HTTPError: ", e.message
        return
    except requests.exceptions.ConnectionError:
        if config["verbose_mode"]:
            print "Connection error for Path: " + str(path)
        return
    if not request.status_code == 200:
        if config["verbose_mode"]:
            print "Expected status 200"
        return
    else:
        data = json.loads(request.text)
        for item in data['result']:
            if config["verbose_mode"]:
                print 'Table: '+ table + ': Raid ID: ' + str(item['id'])

            # These json/hash fields should always be constant in all cases
            id = int(item['id'])
            create_time = str(item['create_time'].strip())
            link = str(item['link'].strip())

            link_name, raid_id, difficulty, raid_boss, raid_boss_human, raid_hash, serverid = get_link_details(link)

            sql = "INSERT INTO %s ( id, create_time, platform, link_name, raid_id, difficulty, \
                raid_boss, raid_boss_human, raid_hash, serverid ) \
                VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ) \
                ON DUPLICATE KEY UPDATE platform='%s', link_name='%s', raid_id='%s', \
                difficulty='%s', raid_boss='%s', raid_boss_human='%s', raid_hash='%s', serverid='%s';" \
                % (table,
                   id, create_time, platform, link_name, raid_id, difficulty, raid_boss, raid_boss_human, raid_hash,
                   serverid,
                   platform, link_name, raid_id, difficulty, raid_boss, raid_boss_human, raid_hash, serverid
                  )

            cursor.execute(sql)
            conn.commit()

# main

build_dictionaries()

ugup_request(shared_api_call_path('raid', 'facebook', 'dawn', 1),   'dawn_shared_raids_fb_s1',    'facebook')
ugup_request(shared_api_call_path('raid', 'facebook', 'dawn', 2),   'dawn_shared_raids_fb_s2',    'facebook')
#
ugup_request(shared_api_call_path('raid', 'facebook', 'suns'),      'suns_shared_raids',          'facebook')


ugup_request(shared_api_call_path('raid', 'armor', 'dawn', 1),      'dawn_shared_raids_armor_s1', 'armor')
ugup_request(shared_api_call_path('raid', 'armor', 'dawn', 2),      'dawn_shared_raids_armor_s2', 'armor')
#
ugup_request(shared_api_call_path('raid', 'armor', 'suns'),         'suns_shared_raids_armor',    'armor')


ugup_request(shared_api_call_path('raid', 'kongregate', 'dawn', 1), 'dawn_shared_raids_kong_s1',  'kongregate')
ugup_request(shared_api_call_path('raid', 'kongregate', 'dawn', 2), 'dawn_shared_raids_kong_s2',  'kongregate')
#
ugup_request(shared_api_call_path('raid', 'kongregate', 'suns'),    'suns_shared_raids_kong',     'kongregate')


ugup_request(shared_api_call_path('raid', 'newgrounds', 'dawn', 1), 'dawn_shared_raids_ng_s1',    'newgrounds')
ugup_request(shared_api_call_path('raid', 'newgrounds', 'dawn', 2), 'dawn_shared_raids_ng_s2',    'newgrounds')
#
ugup_request(shared_api_call_path('raid', 'newgrounds', 'suns'),    'suns_shared_raids_ng',       'newgrounds')

#

cursor.close()
conn.close()

if config["verbose_mode"]:
    print "Job's Done!"
