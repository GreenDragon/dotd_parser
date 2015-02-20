#!/usr/bin/python
#Import equipment from ugup
import yaml
import re
import json
import os
import requests 
import MySQLdb
config = yaml.load(open('/home/www-data/web2py/applications/test/private/apikey').read())
base = 'http://ugup.5thplanetgames.com/api/'
conn = MySQLdb.connect (host = config['dbhost'],
                        user = config['dbuser'],
                        passwd = config['dbpass'],
                        db = config['db'])
cursor = conn.cursor ()
row = cursor.execute("select id from item ORDER BY id DESC LIMIT 1;")
last = cursor.fetchone()
if last == None:
	last = 0
count = last[0] + 1
def item_query(item):
	path = base + item + "all?apikey=" + config["apikey"] + "&platform=" + config["platform"] + "&game=" + config["game"]
	return path

def ugup_request(path, table):
	request = requests.get(path)
	if not request.status_code == 200:
		request.raise_for_status()
	else:
		data = json.loads(request.text)
		for item in data['result']:
			proc_name = re.escape(item['proc_name'])
			name = re.escape(item['name'])
			if table == 'item':
				attack = item['attack']
				defense = item['defense']
				perception = item['perception']
				slot = item['equipType']
				sql = "INSERT into %s (name, proc_name, attack, defense, perception, slot) VALUES ('%s', '%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE slot='%s';" % (table, name, proc_name, attack, defense, perception, slot, slot)
				print sql
				cursor.execute(sql)
			if table == 'general':
				attack = item['attack']
				defense = item['defense']
				race = item['race']
				sql = "INSERT into %s (name, proc_name, attack, defense, race) VALUES ('%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE proc_name='%s';" % (table, name, proc_name, attack, defense, race, proc_name)
				print sql
				cursor.execute(sql)
			if table == 'mount':
				attack = item['attack']
				defense = item['defense']
				perception = item['perception']
				sql = "INSERT into %s (name, proc_name, attack, defense, perception) VALUES ('%s', '%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE proc_name='%s';" % (table, name, proc_name, attack, defense, perception, proc_name )
				print sql
				cursor.execute(sql)
			if table == 'legion':
				sql = "INSERT into %s (name, proc_name) VALUES ('%s', '%s') ON DUPLICATE KEY UPDATE proc_name='%s';" % (table, name, proc_name, proc_name)
				print sql
				cursor.execute(sql)
			if table == 'troop':
                                attack = item['attack']
                                defense = item['defense']
				sql = "INSERT into %s (name, proc_name, attack, defense) VALUES ('%s', '%s', '%s', '%s') ON DUPLICATE KEY UPDATE proc_name='%s';" % (table, name, proc_name, attack, defense, proc_name )
				print sql
				cursor.execute(sql)
		conn.commit()

rurl = item_query('equipment/definition/')
r = ugup_request(rurl, 'item')
rurl = item_query('mount/definition/')
r = ugup_request(rurl, 'mount')
rurl = item_query('general/definition/')
r = ugup_request(rurl, 'general')
rurl = item_query('legion/definition/')
r = ugup_request(rurl, 'legion')
rurl = item_query('troop/definition/')
r = ugup_request(rurl, 'troop')
cursor.close()
conn.close()
