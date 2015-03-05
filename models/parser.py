import locale
import syslog

locale.setlocale(locale.LC_ALL, '')

syslog.openlog(facility=syslog.LOG_USER)

def parser(input):
    experience = {
        "user": "",
        "critical_hits": 0,
        "regular_hits": 0,
        "total_crit_dmg": 0,
        "total_reg_dmg": 0,
        "total_procs": 0,
        "total_proc_dmg": 0,
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
    biggest_hit_suns_mode = 0

    proc_to_names = load_proc_to_names()

    log_file = []
    log_file = input.split('\n')

    for num, line in enumerate(list(log_file)):
        # You Found Orange Scourge Scrap!
        #
        # nil
        if "Found" in line:
            object = line.split('Found')[1][:-2]

            if not object in found_items:
                found_items[object] = 1
            else:
                found_items[object] += 1
            continue

        # You have obtained: Rage of Vigbjorn.
        #
        # You have obtained: Orange Travel Journal.
        if "obtained:" in line:
            object = line.split('obtained:')[1][:-2]

            if not object in obtained_items:
                obtained_items[object] = 1
            else:
                obtained_items[object] += 1
            continue

        # Murder Sanctify (Steed) contributed 51,961,730 damage.
        #
        # Art of War contributed 3,618,250 damage.
        #
        if "contributed" in line:
            #
            # Evil! Take a Chance has contributed additional damage.
            # Evil! Take a Chance has contributed extra damage!
            # Evil! Take a Chance has granted you additional credits!
            #
            object, amount = line.split('contributed')
            object = object.strip()
            amount = amount.strip()

            if amount in [ 'additional damage.', 'extra damage!', 'additional credits!' ]:
                # Treat LoTS contributed events as DotD restored events
                if not line in restored_items:
                    restored_items[line] = 1
                else:
                    restored_items[line] += 1
                continue
            else:
                for proc_name in proc_to_names:
                    if object in proc_name:
                        object = str(proc_name[object])

                amount = int(amount.split()[0].replace(',', ''))

                if not object in proc_items:
                    proc_items[object] = {'count': 1, 'damage': amount}
                else:
                    proc_items[object]['count'] += 1
                    proc_items[object]['damage'] += amount

                experience['total_procs'] += 1
                experience['total_proc_dmg'] += amount

        # Veritas dealt 44,309,515 damage! Lost 5 health. Earned 2,856 gold and 32 experience!
        # Veritas crit 173,145,219 damage! Lost 9 health. Earned 2,968 gold and 35 experience!
        #
        # LoTS mode: Earned 10,406 credits and 29 experience!
        #
        if "experience!" in line:
            # syslog.syslog('Something wicked this way went')
            # is this LoTS? No credits in the DotD world
            if "credits" in line:
                object = line.split()
                for item in 1, 4:
                    amount = int(object[item].replace(',', ''))
                    if item == 1:
                        experience['gold'] +=  amount
                    else:
                        experience['exp'] += amount
            # DoTD mode
            else:
                # watch out for: Take a Chance has granted you additional experience!
                if not "has granted you" in line:
                    object = line.split()
                    experience['user'] = object[0]

                    # store damage dealt in hit_list history line #: damage
                    damage = int(object[2].replace(',', ''))
                    hit_list[num] = damage

                    if "crit" in object[1]:
                        experience['critical_hits'] += 1
                        experience['total_crit_dmg'] += damage
                    else:
                        experience['regular_hits'] += 1
                        experience['total_reg_dmg'] += damage

                    for item in 5, 8, 11:
                        amount = int(object[item].replace(',', ''))
                        if item == 5:
                            experience['health'] += amount
                        elif item == 8:
                            experience['gold'] += amount
                        else:
                            experience['exp'] += amount

        # LoTS Mode
        #
        # KwanSai dealt 154,442,731 health damage! Lost 16 health.
        # KwanSai crit 27,538,998 health damage! Lost 48 health.
        #
        if "health damage" in line:
            object = line.split()

            # store damage dealt in hit_list history line #: damage
            damage = int(object[2].replace(',', ''))
            hit_list[num] = damage

            if "crit" in object[1]:
                experience['critical_hits'] += 1
                experience['total_crit_dmg'] += damage
            else:
                experience['regular_hits'] += 1
                experience['total_reg_dmg'] += damage

            amount = int(object[6].replace(',', ''))
            experience['health'] += amount
            biggest_hit_suns_mode = 1

        # Like a Book has restored some of your Health.
        # Tollo Darkgaze has restored 4 Honor.
        #
        # nil
        if "has restored" in line:
            if not line in restored_items:
                restored_items[line] = 1
            else:
                restored_items[line] += 1
            continue

        # LoTS
        #
        # Take a Chance has granted you additional credits!
        # Take a Chance has granted you additional experience!
        if "has granted you" in line:
            if not line in restored_items:
                restored_items[line] = 1
            else:
                restored_items[line] += 1
            continue

        # Crystal Sight affected boss damage.
        # Bladezz' Blades affected boss damage.
        #
        # nil
        if "affected" in line:
            if not line in affected_items:
                affected_items[line] = 1
            else:
                affected_items[line] += 1
            continue

        # Master of Monsters has created a Steed of the Western Wold!
        #
        # Legacy Forge created a Immortal!
        if "created" in line:
            if not line in created_items:
                created_items[line] = 1
            else:
                created_items[line] += 1
            continue

        # Vigbjorn the Crazed says: "You believe me, Veritas, don't you? We'll hunt the blue yetis together!"
        #
        # nil
        if "says" in line:
            continue

        # *DEV* Mouse applied Magic: Begone, Fiends!
        # *DEV* ryanSMASH applied Magic: Hell's Knell
        if "applied" in line:
            continue

        # If you made it this far, it's either an unknown log line, or garbage

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
    if biggest_hit_suns_mode:
        previous_hit = previous_hit + 1
        biggest_hit = biggest_hit + 1

    for hits in range(previous_hit + 1, biggest_hit + 1):
        max_hit.append(log_file[hits])

    # close out syslog
    syslog.closelog()

    return experience, obtained_items, proc_items, found_items, log_file, max_hit, hit_list, restored_items, \
           affected_items, created_items
