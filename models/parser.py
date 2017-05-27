import locale
import syslog

locale.setlocale(locale.LC_ALL, '')

syslog.openlog(facility=syslog.LOG_USER)

def parser(input):
    experience = {
        "user": "",
        "critical_hits": 0,
        "regular_hits": 0,
        "missed_hits": 0,
        "adventure_hits": 0,
        "shield_hits": 0,
        "total_crit_dmg": 0,
        "total_reg_dmg": 0,
        "total_shield_dmg": 0,
        "total_procs": 0,
        "total_proc_dmg": 0,
        "total_adv_dmg": 0,
        "magic_health_dmg": 0,
        "health": 0,
        "gold": 0,
        "exp": 0,
        "adventure_exp": 0,
    }

    obtained_items = {}
    proc_items = {}
    multi_proc_items = {}
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
    multi_procs_found = 0

    current_hit_count = 1

    proc_name_map = build_proc_name_map()

    log_file = []
    log_file = input.splitlines()

    for num, line in enumerate(list(log_file)):
        line = line.strip()

        # Users have singular names except Devs
        if "damage!" in line:
            line = line.replace("*DEV* ", "*DEV*_", 1)

        # You Found Orange Scourge Scrap!
        #
        # LoTS: nil
        #
        if "Found" in line:
            object = line.split('Found')[1][:-1].strip()

            if object not in found_items:
                found_items[object] = 1
            else:
                found_items[object] += 1

        # You have obtained: Rage of Vigbjorn.
        #
        # You have obtained: Orange Travel Journal.
        # Guster has apologized and given you a Box of Guilt
        elif "obtained:" in line or "given you a" in line:
            if "obtained:" in line:
                object = line.split('obtained:')[1][:-1].strip()
            else:
                object = line.split('given you a')[1].strip()

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
            # Astral Supremacy contributed 10,250,000 damage.
            # Astral Supremacy contributed 779,000 damage.
            # From Money (Diamond Gun) contributed 5,945,000 damage.
            # Alea Iacta Sunt contributed 9,409 damage.
            #
            # Variants
            #
            # Take a Chance has contributed additional damage.
            # Take a Chance has contributed extra damage!
            # Take a Chance has granted you additional credits!
            #
            object, amount = line.split('contributed')
            object = object.strip()
            amount = amount.strip()

            if amount in [ 'additional damage.', 'extra damage!', 'additional credits!' ]:
                # Treat LoTS contributed events as DotD restored events
                # DotD
                #
                # Burning Rain has inflicted additional damage to your enemy. You also sustained 8 damage from the magic.
                #
                # LoTS
                #
                # Scorched Earth has inflicted additional damage to your enemy. You also sustained some damage.
                # Take a Chance has contributed extra damage!
                #
                if line not in restored_items:
                    restored_items[line] = 1
                else:
                    restored_items[line] += 1
            else:
                if len(amount):
                    if isnum(amount.split()[0]):
                        seen_proc_name = object
                        seen_slot_name = 'Unmapped'

                        # This needs to stop descending the tree when proc first found.
                        # Otherwise, the proc_name could map to another object
                        # Memento Mori vs Tuora the Philospher
                        for proc_name in proc_name_map:
                            if object in proc_name:
                                seen_slot_name = str(proc_name[object]['slot'])
                                object = str(proc_name[object]['name'])
                                break

                        amount = int(amount.split()[0].replace(',', ''))

                        if object not in proc_items:
                            proc_items[object] = {'count': 1,
                                                  'damage': amount,
                                                  'damage_seen': [ amount ],
                                                  'proc_name': seen_proc_name,
                                                  'slot': seen_slot_name }
                        else:
                            proc_items[object]['count'] += 1
                            proc_items[object]['damage'] += amount
                            proc_items[object]['damage_seen'].append(amount)

                        # build multiproc table
                        # A New Procer with first hit ever
                        if object not in multi_proc_items:
                            multi_proc_items[object] = {}
                            multi_proc_items[object]['proc_count'] = 1
                            multi_proc_items[object]['multi_hit_counter'] = 0
                            multi_proc_items[object]['hits'] = {}
                            multi_proc_items[object]['hits'][current_hit_count] = [amount]
                        # Known procer with a repeat hit
                        else:
                            multi_proc_items[object]['proc_count'] += 1
                            # If new hit sequence
                            if current_hit_count not in multi_proc_items[object]['hits']:
                                multi_proc_items[object]['hits'][current_hit_count] = [amount]
                            # Else continuing a hit sequence with multi-procs
                            else:
                                multi_proc_items[object]['hits'][current_hit_count].append(amount)
                                if len(multi_proc_items[object]['hits'][current_hit_count]) == 2:
                                    multi_proc_items[object]['multi_hit_counter'] += 1
                                multi_procs_found += 1

                        experience['total_procs'] += 1
                        experience['total_proc_dmg'] += amount
                    else:
                        syslog.syslog(line)
                else:
                    syslog.syslog(str(num) + ": " + line)

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
                object = line.split()

                # Regular hit
                # length = 13
                # Veritas dealt 44,309,515 damage! Lost 5 health. Earned 2,856 gold and 32 experience!
                # Veritas crit 173,145,219 damage! Lost 9 health. Earned 2,968 gold and 35 experience!
                #
                if len(object) == 13:
                    if isnum(object[2]):
                        experience['user'] = object[0]

                        damage = int(object[2].replace(',', ''))

                        # store damage dealt in hit_list history line #: damage
                        hit_list[num] = damage
                        current_hit_count += 1

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

                # Missed on campaign hit
                # length = 11
                # Gwenduin missed! Lost 18 health. Earned 2,250 gold and 27 experience!
                # Fugue missed! Lost 8 health. Earned 1,933 gold and 20 experience!
                #
                elif len(object) == 11 and "missed!" in line:
                    if isnum(object[3]):
                        experience['user'] = object[0]
                        experience['missed_hits'] += 1
                        for item in 3, 6, 9:
                            if isnum(object[item]):
                                amount = int(object[item].replace(',', ''))
                                if item == 3:
                                    experience['health'] += amount
                                elif item == 6:
                                    experience['gold'] += amount
                                else:
                                    experience['exp'] += amount
                            else:
                                syslog.syslog(line)
                    else:
                        syslog.syslog(line)

                # Adventure Mode
                # length = 16
                # Dantro dealt 99,863 damage! Lost 11 health. Earned 2,067 gold, 4 adventurer experience, and 32 experience!
                #
                elif len(object) == 16 and "adventure experience" in line:
                    if isnum(object[2]):
                        experience['user'] = object[0]

                        damage = int(object[2].replace(',', ''))

                        # store damage dealt in hit_list history line #: damage
                        # hit_list[num] = damage

                        experience['adventure_hits'] += 1
                        experience['total_adv_dmg'] += damage

                        for item in 5, 8, 10, 14:
                            if isnum(object[item]):
                                amount = int(object[item].replace(',', ''))
                                if item == 5:
                                    experience['health'] += amount
                                elif item == 8:
                                    experience['gold'] += amount
                                elif item == 10:
                                    experience['adventure_exp'] += amount
                                else:
                                    experience['exp'] += amount
                            else:
                                syslog.syslog(line)
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

            if len(object) == 8:
                experience['user'] = object[0]
                log_suns_mode = 1

                if isnum(object[2]):
                    damage = int(object[2].replace(',', ''))

                    # store damage dealt in hit_list history line #: damage
                    hit_list[num] = damage
                    current_hit_count += 1

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

        # LoTS Mode
        #
        # ShadowFox dealt 451,000 shield damage! Lost 22 health.
        #
        elif "shield damage" in line:
            object = line.split()

            if len(object) == 8:
                experience['user'] = object[0]
                log_suns_mode = 1

                if isnum(object[2]):
                    damage = int(object[2].replace(',', ''))

                    # store damage dealt in hit_list history line #: damage
                    # hit_list[num] = damage

                    experience['shield_hits'] += 1
                    experience['total_shield_dmg'] += damage

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
            restorer, restored = line.split('has restored')
            restorer = restorer.strip()
            restored = restored.strip()
            seen_proc_name = restorer

            for proc_name in proc_name_map:
                if restorer in proc_name:
                    seen_proc_name = str(proc_name[restorer]['name'])
                    break

            mod_line = seen_proc_name + ' has restored ' + restored

            if line not in restored_items:
                restored_items[line] = { 'count': 1,
                                         'desc': mod_line,
                                         'proc_name': restorer,
                                         'proc_owner': seen_proc_name }
            else:
                restored_items[line]['count'] += 1

        # LoTS
        #
        # Take a Chance has granted you additional credits!
        # Take a Chance has granted you additional experience!
        #
        elif "has granted you" in line:
            log_suns_mode = 1
            if line not in restored_items:
                restored_items[line] = 1
            else:
                restored_items[line] += 1


        # Crystal Sight affected boss damage.
        # Bladezz' Blades affected boss damage.
        # Guster has helped you deal some serious damage!
        #
        # nil
        elif any(s in line for s in ('affected', 'has helped you')):
            if "has helped you" in line:
                affector, affected = line.split('has helped you')
                affector = affector.strip()
                affected = affected.strip()
                seen_proc_name = affector

                if "Guster has helped you" in line:
                    # Magic:: Guster's Fault
                    seen_proc_name = "Guster's Fault"
                    affector = seen_proc_name
                else:
                    for proc_name in proc_name_map:
                        if affector in proc_name:
                            seen_proc_name = str(proc_name[affector]['name'])
                            break

                mod_line = seen_proc_name + ' has helped you ' + affected

            else:
                affector, affected = line.split('affected')
                affector = affector.strip()
                affected = affected.strip()
                seen_proc_name = affector

                for proc_name in proc_name_map:
                    if affector in proc_name:
                        seen_proc_name = str(proc_name[affector]['name'])
                        break

                mod_line = seen_proc_name + ' affected ' + affected

            if line not in affected_items:
                affected_items[line] = {'count': 1,
                                        'desc': mod_line,
                                        'proc_name': affector,
                                        'proc_owner': seen_proc_name}
            else:
                affected_items[line]['count'] += 1


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
        # LoTS: ?? || nil
        elif any(s in line for s in ('says', 'yells', 'Mira gives', 'The Dark Lord', 'Dimetrodon', 'DIMETRODON')):
            if line not in rant_items:
                rant_items[line] = 1
            else:
                rant_items[line] += 1

        # *DEV* Mouse applied Magic: Begone, Fiends!
        # *DEV* ryanSMASH applied Magic: Hell's Knell
        #
        # Aura removed Magic: Blood Moon
        #
        # Burning Rain has inflicted additional damage to your enemy. You also sustained 8 damage from the magic.
        #
        elif any(s in line for s in ('applied Magic', 'removed Magic', 'from the magic', 'applied Tactic', 'removed Tactic')):
            if line not in magic_items:
                magic_items[line] = 1
            else:
                magic_items[line] += 1

            if "Burning Rain" in line:
                object = line.split()

                if len(object) == 17:
                    if isnum(object[12]):
                        damage = int(object[12].replace(',', ''))
                        experience['magic_health_dmg'] += damage
                    else:
                        syslog.syslog(line)
                else:
                   syslog.syslog(line)

        # Cooler than Being Cool (Crystal) has triggered a second attack!
        # Haste has triggered a second attack for free!
        #
        elif "triggered" in line:
            if line not in triggered_items:
                triggered_items[line] = 1
            else:
                triggered_items[line] += 1

        # Some players concatenate multiple logs into one stream
        # RikaStormwin dealt 11,590,546 damage!
        # KwanSai dealt 123,063,260 damage!
        #
        elif "dealt" in line and "health" not in line:
            object = line.split()

        # Ouryu crit 16,906,936 damage!
        # MengaoLIGABR crit 68,156,584 damage!
        #
        elif "crit" in line and "health" not in line:
            object = line.split()

        # If we made it this far, it's either an unknown log line, or garbage
        #
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
           affected_items, created_items, rant_items, magic_items, triggered_items, log_suns_mode, \
           multi_procs_found, multi_proc_items
