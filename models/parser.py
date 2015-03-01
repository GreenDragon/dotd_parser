import os
import itertools
import locale

locale.setlocale(locale.LC_ALL, '')

def load_proc_to_names():
    generals_translation = {}
    mounts_translation = {}
    equipment_translation = {}
    troops_translation = {}
    legions_translation = {}

    glist = db().select(db.generals.name, db.generals.proc_name)
    mlist = db().select(db.mounts.name, db.mounts.proc_name)
    ilist = db().select(db.equipment.name, db.equipment.proc_name)
    tlist = db().select(db.troops.name, db.troops.proc_name)
    llist = db().select(db.legions.name, db.legions.proc_name)

    for row in glist:
        generals_translation[row.proc_name] = row.name

    for row in mlist:
        mounts_translation[row.proc_name] = row.name

    for row in ilist:
        equipment_translation[row.proc_name] = row.name

    for row in tlist:
        troops_translation[row.proc_name] = row.name

    for row in llist:
        legions_translation[row.proc_name] = row.name

    translation = [generals_translation, mounts_translation, equipment_translation, troops_translation, legions_translation]
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
    restored_items = {}
    affected_items = {}
    created_items = {}


    max_hit = []
    hit_list = {}

    proc_to_names = load_proc_to_names()

    log_file = []
    log_file = input.split('\n')

    for num, line in enumerate(list(log_file)):
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
                    object = str(proc_name[object])

            amount = int(amount.split()[0].replace(',', ''))

            if not object in proc_items:
                proc_items[object] = {'count': 1, 'damage': amount}
            else:
                proc_items[object]['count'] += 1
                proc_items[object]['damage'] = proc_items[object]['damage'] + amount

        if "experience!" in line:
            object = line.split()
            experience["user"] = object[0]

            # store damage dealt in hit_list history line #: damage
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

        if "has restored" in line:
        #   # Like a Book has restored some of your Health.
        #   # Tollo Darkgaze has restored 4 Honor.
            if not line in restored_items:
                restored_items[line] = 1
            else:
                restored_items[line] += 1

        if "affected" in line:
        #   # Crystal Sight affected boss damage.
        #   # Bladezz' Blades affected boss damage.
            if not line in affected_items:
                affected_items[line] = 1
            else:
                affected_items[line] += 1

        # if "says" in line:
        #   # Vigbjorn the Crazed says: "You believe me, Veritas, don't you? We'll hunt the blue yetis together!"

        # if "applied" in line:
        #   # *DEV* Mouse applied Magic: Begone, Fiends!
        #   # *DEV* ryanSMASH applied Magic: Hell's Knell

        if "has created a" in line:
        #   # Master of Monsters has created a Steed of the Western Wold!
        #   # Master of Monsters has created a Blue Manticore!
        #   # Master of Monsters has created a Floating Eye!
            if not line in created_items:
                created_items[line] = 1
            else:
                created_items[line] += 1

        # LoTS mode
        # if "experience!" in line:
        #   # Earned 1,897 credits and 93 experience!
        # if "health damage" in line:
        #   # KwanSai dealt 154,442,731 health damage! Lost 16 health.
        # if "has granted you" in line:
        #   # Take a Chance has granted you additional credits!
        #   # Take a Chance has granted you additional experience!
        # if "obtained" in line:
        #   # You have obtained: Little Devil.
        #
        # vs DotD mode
        #   # Veritas dealt 38,371,884 damage! Lost 9 health. Earned 3,234 gold and 35 experience!

    # find the biggest hit
    biggest_hit = max(hit_list, key=hit_list.get)

    # build out a history of biggest hit indexes
    hit_indexes = []
    for a in sorted(hit_list.keys()):
        hit_indexes.append(a)

    # find the previous hit before the biggest hit, or just map the current hit
    try:
        previous_hit = hit_indexes[hit_indexes.index(biggest_hit) - 1]
    except ValueError:
        previous_hit = biggest_hit

    # build out the last biggest hit history
    for hits in range(previous_hit + 1, biggest_hit + 1):
        max_hit.append(log_file[hits])

    return experience, obtained_items, proc_items, found_items, log_file, max_hit, hit_list, restored_items, \
           affected_items, created_items
