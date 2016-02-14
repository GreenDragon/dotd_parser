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


def get_dawn_img_url(id, name):
    url = ''
    if int(id) < 29:
        if str(name) == 'Poison':
            name = 'poisonspell_blue'
        if str(name) == 'Greater Poison':
            name = 'poisonspell_red'
        if str(name) == 'Lesser Poison':
            name = 'poisonspell_red'
        if str(name) == 'Midas\' Touch':
            name = 'midashand'
        if str(name) == 'Lesser Impending Doom':
            name = 'impendingdoom_green'
        if str(name) == 'Greater Impending Doom':
            name = 'impendingdoom_red'
        if str(name) == 'Impending Doom':
            name = 'impendingdoom_blue'
        if str(name) == 'Greater Midas\' Touch':
            name = 'greatermidas'
        if str(name) == 'Khan\'s Gift':
            name = 'khans_gift'
        if str(name) == 'Nela\'s Kiss':
            name = 'nelas_kiss'
        url = str(name.replace(' ','').replace("\'",'').replace(".",'').replace("!",'').replace("?",'').replace(",",'').lower()) + '.jpg'
    else:
        if str(name) == 'Annus Mirabilis':
            name = 'annusmirabilis'
        if str(name) == 'Vengeance of the Immortal':
            name = 'immortal'
        if str(name) == 'Melody and Massacre':
            name = 'melody_of_massacre'
        if str(name) == 'Qwil-Killer Fury':
            name = 'qwil_killer_fury'
        if str(name) == 'Dark Fate Unleashed':
            name = 'dark_fate'
        if str(name) == 'Desiccate':
            name = 'desicate'
        if str(name) == 'Purify':
            name = 'purity'
        if str(name) == 'Britton Triumphant':
            name = 'best_that_ever_was'
        url = str(name.replace(' ','_').replace('\'','').replace(".",'').replace("!",'').replace("?",'').replace(",",'').lower()) + '.jpg'
    return str(url)

def get_sun_img_url(id, name):
    url = ''
    #  1:
    if str(name) == 'It\'s a Trap!':
            name = 'itsatrap'
    #  2:
    if str(name) == 'Suppressive Fire':
            name = 'suppressivefire'
    #  3:
    if str(name) == 'Space Raiders':
            name = 'spaceraiders'
    #  4:
    if str(name) == 'Plan 10 from Outer Space':
            name = 'plan10'
    #  5:
    if str(name) == 'Flank Attack':
            name = 'flankattack'
    #  6:
    if str(name) == 'Pursuit of Excellence':
        name = 'pursuitofexcellence'
    #  9: I Have a Cunning Plan... ( ??? )
    # 58: Trick or Treat ( png )
    # 63:     gorgon_s_stare
    if str(name) == 'Gorgon\'s Stare':
            name = 'gorgon_s_stare'
    # 73: Smythe Procedure ( ??? )
    # 75: The Dutch Defense ( png )
    # 78: Mercy Kill ( png )
    # 81: Trojan Horse ( png )
    # 82: Virus ( png )
    if id not in (58,75,78,79,81,82):
        url = str(name.replace(' ','_').replace('\'','').replace(".",'').replace("!",'').replace("?",'').replace(",",'').lower()) + '.jpg'
    else:
        url = str(name.replace(' ','_').replace('\'','').replace(".",'').replace("!",'').replace("?",'').replace(",",'').lower()) + '.png'
    return str(url)


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
            raw_name = item['name'].strip()

            # Raid tables don't have proc info, magic tables don't have proc_name
            if table not in ['dawn_raids', 'suns_raids']:
                if table not in ['dawn_magics', 'suns_magics']:
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

            if table in ['dawn_raids', 'suns_raids']:
                classid = int(item['classid'])
                cooldowntimer = int(item['cooldowntimer'])
                difficulty = re.escape(json.dumps(item['difficulty']))
                energy = int(item['energy'])
                guildraid = int(item['guildraid'])
                honor = int(item['honor'])
                icon = re.escape(item['icon'].strip())
                image = re.escape(item['image'].strip())
                maxattackers = int(item['maxattackers'])
                # name = re.escape(item['name'].strip())
                numdebuffs = int(item['numdebuffs'])
                postimage = str(item['postimage'].strip().split('post/')[1])
                races = re.escape(item['races'].strip())
                raidtimer = int(item['raidtimer'])
                shortname = re.escape(item['shortname'].strip())
                size = int(item['size'])
                stamina = int(item['stamina'])

                sql = "INSERT INTO %s ( id, classid, cooldowntimer, difficulty, energy, guildraid, honor, icon, \
                       image, maxattackers, name, numdebuffs, postimage, races, raidtimer, shortname, size, stamina ) \
                       VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', \
                       '%s', '%s', '%s', '%s' ) \
                       ON DUPLICATE KEY UPDATE classid='%s', cooldowntimer='%s', difficulty='%s', energy='%s', \
                       guildraid='%s', honor='%s', icon='%s', image='%s', maxattackers='%s', name='%s', \
                       numdebuffs='%s', postimage='%s', races='%s', raidtimer='%s', shortname='%s', size='%s', \
                       stamina='%s';" \
                       % ( table, id, classid, cooldowntimer, difficulty, energy, guildraid, honor, icon,
                       image, maxattackers, name, numdebuffs, postimage, races, raidtimer, shortname, size,
                       stamina, classid, cooldowntimer, difficulty, energy, guildraid, honor, icon, image,
                       maxattackers, name, numdebuffs, postimage, races, raidtimer, shortname, size, stamina )

                cursor.execute(sql)

            if table in ['dawn_magics', 'suns_magics']:
                lore = re.escape(item['lore'].strip())
                questReq = int(item['questReq'])
                rarity = int(item['rarity'])
                value_credits = int(item['value_credits'])
                value_gold = int(item['value_gold'])
                if table == 'dawn_magics':
                    img_url = str(get_dawn_img_url(id, raw_name))
                else:
                    img_url = str(get_sun_img_url(id, raw_name))

                sql = "INSERT INTO %s ( id, lore, name, proc_desc, questReq, rarity, value_credits, value_gold, \
                       img_url ) \
                       VALUES ( '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s' ) \
                       ON DUPLICATE KEY UPDATE lore='%s', name='%s', proc_desc='%s', questReq='%s', \
                       rarity='%s', value_credits='%s', value_gold='%s', img_url='%s';" \
                       % ( table,
                           id, lore, name, proc_desc, questReq, rarity, value_credits, value_gold, img_url,
                           lore, name, proc_desc, questReq, rarity, value_credits, value_gold, img_url
                         )

                cursor.execute(sql)
            conn.commit()

# main

ugup_request(api_call_path('enchant', 'dawn'), 'dawn_enchantments')
ugup_request(api_call_path('equipment', 'dawn'), 'dawn_equipment')
ugup_request(api_call_path('general', 'dawn'), 'dawn_generals')
ugup_request(api_call_path('legion', 'dawn'), 'dawn_legions')
ugup_request(api_call_path('mount', 'dawn'), 'dawn_mounts')
ugup_request(api_call_path('troop', 'dawn'), 'dawn_troops')
ugup_request(api_call_path('raid', 'dawn'), 'dawn_raids')
ugup_request(api_call_path('magic', 'dawn'), 'dawn_magics')

ugup_request(api_call_path('enchant', 'suns'), 'suns_enchantments')
ugup_request(api_call_path('equipment', 'suns'), 'suns_equipment')
ugup_request(api_call_path('general', 'suns'), 'suns_generals')
ugup_request(api_call_path('legion', 'suns'), 'suns_legions')
ugup_request(api_call_path('mount', 'suns'), 'suns_mounts')
ugup_request(api_call_path('troop', 'suns'), 'suns_troops')
ugup_request(api_call_path('engineering', 'suns'), 'suns_engineering')
ugup_request(api_call_path('raid', 'suns'), 'suns_raids')
ugup_request(api_call_path('magic', 'suns'), 'suns_magics')

cursor.close()
conn.close()

if config["verbose_mode"]:
    print "Job's Done!"
