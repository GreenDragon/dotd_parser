#!/usr/bin/env python

# Import all tables from ugup that have proc_name mappings

import yaml
import re
import json
import requests
import MySQLdb as mdb
# from pprint import pprint

config = yaml.load(open('../private/apikey').read())

base = 'http://ugup.5thplanetgames.com/api/'

conn = mdb.connect(host=config['dbhost'],
                   user=config['dbuser'],
                   passwd=config['dbpass'],
                   db=config['db'],
                   charset='utf8',
                   use_unicode=True)

cursor = conn.cursor()

def api_call_path(item, game):
    path = base + item + "/definition/all?apikey=" + config["apikey"] \
           + "&platform=" + config["platform"] + "&game=" + game
    return path

def ugup_request(path, table):
    request = requests.get(path)
    if not request.status_code == 200:
        request.raise_for_status()
    else:
        data = json.loads(request.text)
        for item in data['result']:
            if config["verbose_mode"]:
                try:
                    print table + ': ' + str(item['id']) + ': ' + item['name']
                except UnicodeEncodeError:
                    print table + ': ' + str(item['id']) + ': UnicodeEncodeError'

            # These json/hash fields should always be constant in all cases
            id = int(item['id'])
            name = re.escape(item['name'].strip())
            proc_name = re.escape(item['proc_name'].strip())
            proc_desc = re.escape(item['proc_desc'].strip())

            if table in ['dawn_enchantments', 'suns_enchantments']:
                sql = "INSERT INTO %s ( id, name, proc_name, proc_desc ) \
                    VALUES ( '%s', '%s', '%s', '%s') \
                    ON DUPLICATE KEY UPDATE name='%s',proc_name='%s',proc_desc='%s';" \
                    % (table, id, name, proc_name, proc_desc, name, proc_name, proc_desc)

                cursor.execute(sql)

            if table in ['dawn_equipment', 'suns_equipment']:
                attack = int(item['attack'])
                defense = int(item['defense'])
                perception = int(item['perception'])
                rarity = int(item['rarity'])
                value_gold = int(item['value_gold'])
                value_credits = int(item['value_credits'])
                value_gtoken = int(item['value_gtoken'])
                questReq = int(item['questReq'])
                isUnique = int(item['unique'])
                canEnchant = int(item['canEnchant'])
                equipType = int(item['equipType'])
                hlt = int(item['hlt'])
                eng = int(item['eng'])
                sta = int(item['sta'])
                hnr = int(item['hnr'])
                atk = int(item['atk'])
                defn = int(item['def'])
                power = int(item['power'])
                dmg = int(item['dmg'])
                deflect = int(item['deflect'])
                lore = re.escape(item['lore'].strip())

                sql = "INSERT INTO %s ( id, name, attack, defense, perception, rarity, value_gold, value_credits, \
                       value_gtoken, questReq, isUnique, canEnchant, equipType, hlt, eng, sta, hnr, atk, defn, power, \
                       dmg, deflect, lore, proc_name, proc_desc ) \
                       VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                       '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ) \
                       ON DUPLICATE KEY UPDATE name='%s', attack='%s', defense='%s', perception='%s', rarity='%s', \
                       value_gold='%s', value_credits='%s', value_gtoken='%s', questReq='%s', isUnique='%s', \
                       canEnchant='%s', equipType='%s', hlt='%s', eng='%s', sta='%s', hnr='%s', atk='%s', defn='%s', \
                       power='%s', dmg='%s', deflect='%s', lore='%s', proc_name='%s', proc_desc='%s';" \
                       % ( table, id, name, attack, defense, perception, rarity, value_gold, value_credits,
                           value_gtoken, questReq, isUnique, canEnchant, equipType, hlt, eng, sta, hnr, atk, defn,
                           power, dmg, deflect, lore, proc_name, proc_desc, name, attack, defense, perception, rarity,
                           value_gold, value_credits, value_gtoken, questReq, isUnique, canEnchant, equipType, hlt,
                           eng, sta, hnr, atk, defn, power, dmg, deflect, lore, proc_name, proc_desc)

                cursor.execute(sql)

            if table in ['dawn_generals', 'suns_generals']:
                attack = int(item['attack'])
                defense = int(item['defense'])
                race = int(item['race'])
                role = int(item['role'])
                rarity = int(item['rarity'])
                value_gold = int(item['value_gold'])
                value_credits = int(item['value_credits'])
                questReq = int(item['questReq'])
                source = int(item['source'])
                buffType = int(item['buffType'])
                lore = re.escape(item['lore'].strip())

                sql = "INSERT INTO %s ( id, name, attack, defense, race, role, rarity, value_gold, value_credits, \
                       questReq, source, buffType, lore, proc_name, proc_desc ) \
                       VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                       '%s' ) \
                       ON DUPLICATE KEY UPDATE name='%s', attack='%s', defense='%s', race='%s', role='%s', \
                       rarity='%s', value_gold='%s', value_credits='%s', questReq='%s', source='%s', buffType='%s', \
                       lore='%s', proc_name='%s', proc_desc='%s';" \
                       % ( table, id, name, attack, defense, race, role, rarity, value_gold, value_credits, questReq,
                           source, buffType, lore, proc_name, proc_desc, name, attack, defense, race, role,
                           rarity, value_gold, value_credits, questReq, source, buffType, lore, proc_name, proc_desc )

                cursor.execute(sql)

            if table in ['dawn_legions', 'suns_legions']:
                num_gen = int(item['num_gen'])
                num_trp = int(item['num_trp'])
                bonus = int(item['bonus'])
                bonusSpecial = int(item['bonusSpecial'])
                bonusText = re.escape(item['bonusText'].strip())
                rarity = int(item['rarity'])
                value_gold = int(item['value_gold'])
                value_credits = int(item['value_credits'])
                canPurchase = int(item['canpurchase'])
                questReq = int(item['questReq'])
                lore = re.escape(item['lore'].strip())
                # check for JSON mangling in DB here
                specification = re.escape(item['specification'].strip())
                general_format = re.escape(json.dumps(item['general_format']))
                troop_format = re.escape(json.dumps(item['troop_format']))

                sql = "INSERT into %s ( id, name, num_gen, num_trp, bonus, bonusSpecial, bonusText, rarity, value_gold, \
                       value_credits, canPurchase, questReq, lore, proc_name, proc_desc, specification, \
                       general_format, troop_format ) \
                       VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                       '%s', '%s', '%s', '%s' ) \
                       ON DUPLICATE KEY UPDATE name='%s', num_gen='%s', num_trp='%s', bonus='%s', bonusSpecial='%s', \
                       bonusText='%s', rarity='%s', value_gold='%s', value_credits='%s', canPurchase='%s', \
                       questReq='%s', lore='%s', proc_name='%s', proc_desc='%s', specification='%s', \
                       general_format='%s', troop_format='%s';" \
                       % ( table, id, name, num_gen, num_trp, bonus, bonusSpecial, bonusText, rarity, value_gold,
                          value_credits, canPurchase, questReq, lore, proc_name, proc_desc, specification,
                          general_format, troop_format, name, num_gen, num_trp, bonus, bonusSpecial, bonusText,
                          rarity, value_gold, value_credits, canPurchase, questReq, lore, proc_name, proc_desc,
                          specification, general_format, troop_format)

                cursor.execute(sql)

            if table in ['dawn_mounts', 'suns_mounts']:
                attack = int(item['attack'])
                defense = int(item['defense'])
                perception = int(item['perception'])
                rarity = int(item['rarity'])
                value_gold = int(item['value_gold'])
                value_credits = int(item['value_credits'])
                questReq = int(item['questReq'])
                isUnique = int(item['unique'])
                hlt = int(item['hlt'])
                eng = int(item['eng'])
                sta = int(item['sta'])
                hnr = int(item['hnr'])
                atk = int(item['atk'])
                defn = int(item['def'])
                power = int(item['power'])
                dmg = int(item['dmg'])
                deflect = int(item['deflect'])
                lore = re.escape(item['lore'].strip())

                sql = "INSERT INTO %s ( id, name, attack, defense, perception, rarity, value_gold, value_credits, \
                       questReq, isUnique, hlt, eng, sta, hnr, atk, defn, power, dmg, deflect, lore, proc_name, \
                       proc_desc ) \
                       VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                       '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ) \
                       ON DUPLICATE KEY UPDATE name='%s', attack='%s', defense='%s', perception='%s', rarity='%s', \
                       value_gold='%s', value_credits='%s', questReq='%s', isUnique='%s', hlt='%s', eng='%s', \
                       sta='%s', hnr='%s', atk='%s', defn='%s', power='%s', dmg='%s', deflect='%s', lore='%s', \
                       proc_name='%s', proc_desc='%s';" \
                       % ( table, id, name, attack, defense, perception, rarity, value_gold, value_credits, questReq,
                           isUnique, hlt, eng, sta, hnr, atk, defn, power, dmg, deflect, lore, proc_name, proc_desc,
                           name, attack, defense, perception, rarity, value_gold, value_credits, questReq, isUnique,
                           hlt, eng, sta, hnr, atk, defn, power, dmg, deflect, lore, proc_name, proc_desc )

                cursor.execute(sql)

            if table in ['dawn_troops', 'suns_troops']:
                attack = int(item['attack'])
                defense = int(item['defense'])
                race = int(item['race'])
                role = int(item['role'])
                rarity = int(item['rarity'])
                value_gold = int(item['value_gold'])
                value_credits = int(item['value_credits'])
                canPurchase = int(item['canpurchase'])
                questReq = int(item['questReq'])
                source = int(item['source'])
                buffType = int(item['buffType'])
                lore = re.escape(item['lore'].strip())

                sql = "INSERT INTO %s ( id, name, attack, defense, race, role, rarity, value_gold, value_credits, \
                       canPurchase, questReq, source, buffType, lore, proc_name, proc_desc ) \
                       VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                       '%s', '%s' ) \
                       ON DUPLICATE KEY UPDATE name='%s', attack='%s', defense='%s', race='%s', role='%s', \
                       rarity='%s', value_gold='%s', value_credits='%s', canPurchase='%s', questReq='%s', source='%s', \
                       buffType='%s', lore='%s', proc_name='%s', proc_desc='%s';" \
                       % ( table, id, name, attack, defense, race, role, rarity, value_gold, value_credits,
                           canPurchase, questReq, source, buffType, lore, proc_name, proc_desc, name, attack,
                           defense, race, role, rarity, value_gold, value_credits, canPurchase, questReq, source,
                           buffType, lore, proc_name, proc_desc )

                cursor.execute(sql)

            if table in ['suns_engineering']:
                attack = int(item['attack'])
                defense = int(item['defense'])
                engineering = int(item['engineering'])
                value_credits = int(item['value_credits'])
                isUnique = int(item['unique'])
                lore = re.escape(item['lore'].strip())
                bonus = re.escape(json.dumps(item['bonus']))

                sql = "INSERT INTO %s ( id, name, attack, defense, engineering, value_credits, isUnique, lore, \
                       proc_name, proc_desc, bonus ) \
                       VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ) \
                       ON DUPLICATE KEY UPDATE name='%s', attack='%s', defense='%s', engineering='%s', \
                       value_credits='%s', isUnique='%s', lore='%s', proc_name='%s', proc_desc='%s', bonus='%s';" \
                       % ( table, id, name, attack, defense, engineering, value_credits, isUnique, lore,
                       proc_name, proc_desc, bonus, name, attack, defense, engineering, value_credits, isUnique, lore,
                       proc_name, proc_desc, bonus )

                cursor.execute(sql)


    conn.commit()

# main

ugup_request(api_call_path('enchant', 'dawn'), 'dawn_enchantments')
ugup_request(api_call_path('equipment', 'dawn'), 'dawn_equipment')
ugup_request(api_call_path('general', 'dawn'), 'dawn_generals')
ugup_request(api_call_path('legion', 'dawn'), 'dawn_legions')
ugup_request(api_call_path('mount', 'dawn'), 'dawn_mounts')
ugup_request(api_call_path('troop', 'dawn'), 'dawn_troops')

ugup_request(api_call_path('enchant', 'suns'), 'suns_enchantments')
ugup_request(api_call_path('equipment', 'suns'), 'suns_equipment')
ugup_request(api_call_path('general', 'suns'), 'suns_generals')
ugup_request(api_call_path('legion', 'suns'), 'suns_legions')
ugup_request(api_call_path('mount', 'suns'), 'suns_mounts')
ugup_request(api_call_path('troop', 'suns'), 'suns_troops')
ugup_request(api_call_path('engineering', 'suns'), 'suns_engineering')

cursor.close()
conn.close()

print "Job's Done!"
