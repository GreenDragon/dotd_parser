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

    # current_hit = 1

    obtained_items = {}
    proc_items = {}
    found_items = {}
    restored_items = {}
    affected_items = {}
    created_items = {}
    rant_items = {}
    magic_items = {}
    triggered_items = {}


    max_hit = []
    hit_list = {}
    log_suns_mode = 0

    proc_to_names = load_proc_to_names()

    log_file = []
    log_file = input.splitlines()

    for num, line in enumerate(list(log_file)):
        line = line.strip()
        # You Found Orange Scourge Scrap!
        #
        # nil
        if "Found" in line:
            object = line.split('Found')[1][:-1].strip()

            if object not in found_items:
                found_items[object] = 1
            else:
                found_items[object] += 1

        # You have obtained: Rage of Vigbjorn.
        #
        # You have obtained: Orange Travel Journal.
        elif "obtained:" in line:
            object = line.split('obtained:')[1][:-1].strip()

            if object not in obtained_items:
                obtained_items[object] = 1
            else:
                obtained_items[object] += 1

        # Murder Sanctify (Steed) contributed 51,961,730 damage.
        #
        # Art of War contributed 3,618,250 damage.
        #
        elif "contributed" in line:
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
                if line not in restored_items:
                    restored_items[line] = 1
                else:
                    restored_items[line] += 1
            else:
                if isnum(amount.split()[0]):
                    seen_proc_name = object
                    for proc_name in proc_to_names:
                        if object in proc_name:
                            object = str(proc_name[object])

                    amount = int(amount.split()[0].replace(',', ''))

                    if object not in proc_items:
                        proc_items[object] = {'count': 1,
                                              'damage': amount,
                                              'damage_seen': [ amount ],
                                              'proc_name': seen_proc_name }
                        # 'hits_seen': [ current_hit ]}
                    else:
                        proc_items[object]['count'] += 1
                        proc_items[object]['damage'] += amount
                        proc_items[object]['damage_seen'].append(amount)
                        # proc_items[object]['hits_seen'].append(current_hit)

                    experience['total_procs'] += 1
                    experience['total_proc_dmg'] += amount
                else:
                    syslog.syslog(line)

        #
        elif "experience!" in line and "granted" not in line:
            # Is this LoTS? No credits in the DotD world
            #
            # Earned 10,406 credits and 29 experience!
            #
            if "credits" in line:
                object = line.split()

                if len(object) == 6 and object[0] == 'Earned':
                    for item in 1, 4:
                        if isnum(object[item]):
                            amount = int(object[item].replace(',', ''))
                            if item == 1:
                                experience['gold'] +=  amount
                            else:
                                experience['exp'] += amount
                        else:
                            syslog.syslog(line)
                else:
                    syslog.syslog(line)
            else:
                # DotD Mode
                #
                # Veritas dealt 44,309,515 damage! Lost 5 health. Earned 2,856 gold and 32 experience!
                # Veritas crit 173,145,219 damage! Lost 9 health. Earned 2,968 gold and 35 experience!
                #
                object = line.split()

                if isnum(object[2]):
                    experience['user'] = object[0]

                    damage = int(object[2].replace(',', ''))

                    # store damage dealt in hit_list history line #: damage
                    hit_list[num] = damage
                    # current_hit += 1

                    if "crit" in object[1]:
                        experience['critical_hits'] += 1
                        experience['total_crit_dmg'] += damage
                    else:
                        experience['regular_hits'] += 1
                        experience['total_reg_dmg'] += damage

                    for item in 5, 8, 11:
                        if isnum(object[item]):
                            amount = int(object[item].replace(',', ''))
                            if item == 5:
                                experience['health'] += amount
                            elif item == 8:
                                experience['gold'] += amount
                            else:
                                experience['exp'] += amount
                        else:
                            syslog.syslog(line)
                else:
                    syslog.syslog(line)

        # LoTS Mode
        #
        # KwanSai dealt 154,442,731 health damage! Lost 16 health.
        # KwanSai crit 27,538,998 health damage! Lost 48 health.
        #
        elif "health damage" in line:
            object = line.split()

            if len(object) >= 7:
                experience['user'] = object[0]
                log_suns_mode = 1

                if isnum(object[2]):
                    damage = int(object[2].replace(',', ''))

                    # store damage dealt in hit_list history line #: damage
                    hit_list[num] = damage
                    # current_hit += 1

                    if "crit" in object[1]:
                        experience['critical_hits'] += 1
                        experience['total_crit_dmg'] += damage
                    else:
                        experience['regular_hits'] += 1
                        experience['total_reg_dmg'] += damage

                    if isnum(object[6]):
                        amount = int(object[6].replace(',', ''))
                        experience['health'] += amount
                    else:
                        syslog.syslog(line)
                else:
                    syslog.syslog(line)
            else:
                syslog.syslog(line)

        # DotD
        #
        # Like a Book has restored some of your Health.
        # Tollo Darkgaze has restored 4 Honor.
        #
        elif "has restored" in line:
            if line not in restored_items:
                restored_items[line] = 1
            else:
                restored_items[line] += 1

        # LoTS
        #
        # Take a Chance has granted you additional credits!
        # Take a Chance has granted you additional experience!
        #
        elif "has granted you" in line:
            if line not in restored_items:
                restored_items[line] = 1
            else:
                restored_items[line] += 1


        # Crystal Sight affected boss damage.
        # Bladezz' Blades affected boss damage.
        #
        # nil
        elif "affected" in line:
            if line not in affected_items:
                affected_items[line] = 1
            else:
                affected_items[line] += 1

        # Master of Monsters has created a Steed of the Western Wold!
        #
        # Legacy Forge created a Immortal!
        elif "created" in line:
            if line not in created_items:
                created_items[line] = 1
            else:
                created_items[line] += 1

        # Vigbjorn the Crazed says: "You believe me, Veritas, don't you? We'll hunt the blue yetis together!"
        #
        # nil
        elif "says" in line:
            if line not in rant_items:
                rant_items[line] = 1
            else:
                rant_items[line] += 1

        # *DEV* Mouse applied Magic: Begone, Fiends!
        # *DEV* ryanSMASH applied Magic: Hell's Knell
        # Aura removed Magic: Blood Moon
        elif "applied" in line or "removed" in line:
            if line not in magic_items:
                magic_items[line] = 1
            else:
                magic_items[line] += 1

        # Cooler than Being Cool (Crystal) has triggered a second attack!
        # Haste has triggered a second attack for free!
        elif "triggered" in line:
            if line not in triggered_items:
                triggered_items[line] = 1
            else:
                triggered_items[line] += 1

        # Info from second attack proc?
        # RikaStormwin dealt 11,590,546 damage!
        # KwanSai dealt 123,063,260 damage!
        elif "dealt" in line and "health" not in line:
            object = line.split()

            if len(object) == 4 and object[3] == 'damage!':
                username = object[0].strip()
                # this logic won't work until a second experience round comes along.
                # need a better algorithm here
                # oh well, 80-20 rules...
                if username == experience['user']:
                    if isnum(object[2]):
                        damage = int(object[2].replace(',', ''))

                        experience['regular_hits'] += 1
                        experience['total_reg_dmg'] += damage
                    else:
                        syslog.syslog(line)
                else:
                    syslog.syslog(line)
            else:
                syslog.syslog(line)

        # Info from second attack proc? or another user
        # Ouryu crit 16,906,936 damage!
        # MengaoLIGABR crit 68,156,584 damage!
        elif "crit" in line and "health" not in line:
            object = line.split()

            if len(object) == 4 and object[3] == 'damage!':
                username = object[0].strip()
                # this logic won't work until a second experience round comes along.
                # need a better algorithm here
                # oh well, 80-20 rules...
                if username == experience['user']:
                    if isnum(object[2]):
                        damage = int(object[2].replace(',', ''))

                        experience['critical_hits'] += 1
                        experience['total_crit_dmg'] += damage
                    else:
                        syslog.syslog(line)
                else:
                    syslog.syslog(line)
            else:
                syslog.syslog(line)

        # If we made it this far, it's either an unknown log line, or garbage
        else:
            syslog.syslog(line)

    if len(hit_list):
        # find the biggest hit
        biggest_hit_idx = max(hit_list, key=hit_list.get)

        # build out a history of hit indexes
        hit_indexes = []
        hit_indexes = sorted(hit_list.keys())

        # find the previous hit before the biggest hit, or just map the current hit
        previous_hit_idx = hit_indexes[(hit_indexes.index(biggest_hit_idx) - 1)]

        # it may be the first hit was the biggest, or it was the only hit
        if previous_hit_idx >= biggest_hit_idx:
            previous_hit_idx = 0

        # determine indexes for the biggest hit history
        if log_suns_mode:
            biggest_hit_idx += 1
            if previous_hit_idx != 0:
                previous_hit_idx += 2
        elif previous_hit_idx != 0:
            previous_hit_idx += 1

        for hits in range(previous_hit_idx, biggest_hit_idx + 1):
            try:
                max_hit.append(log_file[hits])
            except IndexError:
                syslog.syslog("Expected one more line from the log file")

    # close out syslog
    syslog.closelog()

    return experience, obtained_items, proc_items, found_items, log_file, max_hit, hit_list, restored_items, \
           affected_items, created_items, rant_items, magic_items, triggered_items, log_suns_mode
