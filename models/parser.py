import os
import itertools
import locale

locale.setlocale(locale.LC_ALL, '')

def load_proc_to_names():
    general_translation = {}
    mount_translation = {}
    item_translation = {}
    troop_translation = {}
    legion_translation = {}

    glist = db().select(db.general.name, db.general.proc_name)
    mlist = db().select(db.mount.name, db.mount.proc_name)
    ilist = db().select(db.item.name, db.item.proc_name)
    tlist = db().select(db.troop.name, db.troop.proc_name)
    llist = db().select(db.legion.name, db.legion.proc_name)

    for row in glist:
        general_translation[row.proc_name] = row.name

    for row in mlist:
        mount_translation[row.proc_name] = row.name

    for row in ilist:
        item_translation[row.proc_name] = row.name

    for row in tlist:
        troop_translation[row.proc_name] = row.name

    for row in llist:
        legion_translation[row.proc_name] = row.name

    translation = [general_translation, mount_translation, item_translation, troop_translation, legion_translation]
    return translation


def parser(input):
    experience = {
        "user": "",
        "critical": 0,
        "regular": 0,
        "crit_damage": 0,
        "damage": 0,
        "health": 0,
        "gold": 0,
        "exp": 0,
    }

    obtained_items = {}
    proc_items = {}
    found_items = {}

    max_hit = ""
    hit_list = {}

    #
    proc_to_names = load_proc_to_names()

    log_entries = {}
    log_entries = list(input.split('\n'))

    for num, line in enumerate(log_entries):
        if "Found" in line:
            object = line.split('Found')[1][:-2]

            if not object in found_items:
                found_items[object] = 1
            else:
                found_items[object] += 1

        if "obtained" in line:
            object = line.split('obtained:')[1][:-2]

            if not object in obtained_items:
                obtained_items[object] = 1
            else:
                obtained_items[object] += 1

        if "contributed" in line:
            object, amount = line.split('contributed')
            object = object.strip()

            for proc_name in proc_to_names:
                if object in proc_name:
                    object = proc_name[str(object)]

            amount = int(amount.split()[0].replace(',', ''))

            if not object in proc_items:
                proc_items[object] = {'count': 1, 'damage': amount}
            else:
                proc_items[object]['count'] += 1
                proc_items[object]['damage'] = proc_items[object]['damage'] + amount

        if "experience!" in line:
            object = line.split()
            experience["user"] = object[0]

            # store damage dealt hit_list history
            damage = int(object[2].replace(',', ''))
            hit_list[num] = damage

            if "crit" in object[1]:
                experience["critical"] += 1
                experience["crit_damage"] = experience["crit_damage"] + damage
            else:
                experience["regular"] += 1
                experience["damage"] = experience["damage"] + damage

            for item in 5, 8, 11:
                amount = int(object[item].replace(',', ''))
                if item == 5:
                    experience["health"] = experience["health"] + amount
                elif item == 8:
                    experience["gold"] = experience["gold"] + amount
                else:
                    experience["exp"] = experience["exp"] + amount

        # if "restored" in line:
        #   # Like a Book has restored some of your Health.
        #   # Tollo Darkgaze has restored 4 Honor.

        # if "affected" in line:
        #   # Crystal Sight affected boss damage.
        #   # Bladezz' Blades affected boss damage.

        # if "says" in line:
        #   # Vigbjorn the Crazed says: "You believe me, Veritas, don't you? We'll hunt the blue yetis together!"

        # if "applied" in line:
        #   # *DEV* Mouse applied Magic: Begone, Fiends!
        #   # *DEV* ryanSMASH applied Magic: Hell's Knell

        # if "created" in line:
        #   # Master of Monsters has created a Steed of the Western Wold!
        #   # Master of Monsters has created a Blue Manticore!
        #   # Master of Monsters has created a Floating Eye!


    # build out history of biggest hit
    max_hit = max(hit_list, key=hit_list.get)

    experience_lines = []

    for a in sorted(hit_list.keys()):
        experience_lines.append(a)

    try:
        previous_hit = experience_lines[experience_lines.index(max_hit) - 1]
    except ValueError:
        previous_hit = max_hit

    highest_damage_lines = []

    for hits in range(previous_hit + 1, max_hit + 1):
        highest_damage_lines.append(log_entries[hits])

    max_hit = highest_damage_lines

    return experience, obtained_items, proc_items, found_items, log_file, max_hit, hit_list
