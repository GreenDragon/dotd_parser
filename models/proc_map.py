def build_proc_name_map():
    generals_dict = {}
    mounts_dict = {}
    equipment_dict = {}
    troops_dict = {}
    legions_dict = {}
    enchantments_dict = {}
    engineering_dict = {}

    armaments_dict = {}

    for row in db().select(db.dawn_generals.name, db.dawn_generals.proc_name):
        if len(row.proc_name):
            generals_dict[row.proc_name] = { 'name':row.name, 'slot':'General' }

    for row in db().select(db.suns_generals.name, db.suns_generals.proc_name, ):
        if len(row.proc_name):
            generals_dict[row.proc_name] = { 'name':row.name, 'slot':'Officer' }

    for row in db().select(db.dawn_mounts.name, db.dawn_mounts.proc_name):
        if len(row.proc_name):
            mounts_dict[row.proc_name] = { 'name':row.name, 'slot':'Mount' }

    for row in db().select(db.suns_mounts.name, db.suns_mounts.proc_name):
        if len(row.proc_name):
            mounts_dict[row.proc_name] = { 'name':row.name, 'slot':'Utility' }

    for row in db().select(db.dawn_equipment.name, db.dawn_equipment.proc_name, db.dawn_equipment.equipType):
        if len(row.proc_name):
            equipment_dict[row.proc_name] = { 'name':row.name, 'slot':get_dawn_equip_name(row.equipType) }

    # main hand, off hand, helmet, chest, gloves, pants, boots, trinket, sidekick, utility, tactic
    # trinket = ring?
    for row in db().select(db.suns_equipment.name, db.suns_equipment.proc_name, db.suns_equipment.equipType):
        if len(row.proc_name):
            equipment_dict[row.proc_name] = { 'name':row.name, 'slot':get_sun_equip_name(row.equipType) }

    for row in db().select(db.dawn_troops.name, db.dawn_troops.proc_name):
        if len(row.proc_name):
            troops_dict[row.proc_name] = { 'name':row.name, 'slot':'Troop' }

    for row in db().select(db.suns_troops.name, db.suns_troops.proc_name):
        if len(row.proc_name):
            troops_dict[row.proc_name] = { 'name':row.name, 'slot':'Crew' }

    for row in db().select(db.dawn_legions.name, db.dawn_legions.proc_name):
        if len(row.proc_name):
            legions_dict[row.proc_name] = { 'name':row.name, 'slot':'Legion' }

    for row in db().select(db.suns_legions.name, db.suns_legions.proc_name):
        if len(row.proc_name):
            legions_dict[row.proc_name] = { 'name':row.name, 'slot':'Ship' }

    for row in db().select(db.dawn_enchantments.name, db.dawn_enchantments.proc_name):
        if len(row.proc_name):
            enchantments_dict[row.proc_name] = { 'name':row.name, 'slot':'Rune' }

    for row in db().select(db.suns_enchantments.name, db.suns_enchantments.proc_name):
        if len(row.proc_name):
            enchantments_dict[row.proc_name] = { 'name':row.name, 'slot':'Crystal' }

    for row in db().select(db.suns_engineering.name, db.suns_engineering.proc_name, db.suns_engineering.engineering):
        if len(row.proc_name):
            engineering_dict[row.proc_name] = { 'name':row.name, 'slot':get_suns_engineer_name(row.engineering) }

    # http://dotd.wikia.com/wiki/Category:Armaments
    #
    # armaments_dict[""] = { 'name':"Armorskin Charm", 'slot':'Armament::Support'}
    armaments_dict["Arrow'd"] = { 'name':"Ballista", 'slot':'Armament::Siege'}
    armaments_dict["Who's There"] = { 'name':"Battering Ram", 'slot':'Armament::Siege'}
    armaments_dict["Scream and Shout"] = { 'name':"Berserker's Horn", 'slot':'Armament::Relic'}
    armaments_dict["BOOM"] = { 'name':"Black Powder", 'slot':'Armament::Siege'}
    # armaments_dict[""] = { 'name':"Blessing of Karuss", 'slot':'Armament::Support'}
    armaments_dict["Heads Up"] = { 'name':"Catapult", 'slot':'Armament::Siege'}
    armaments_dict["Fervor"] = { 'name':"Cermarina's Blade", 'slot':'Armament::Relic'}
    armaments_dict["I'm Back"] = { 'name':"Curse of Returning", 'slot':'Armament::Support'}
    armaments_dict["Biological Warfare"] = { 'name':"Diseased Corpses", 'slot':'Armament::Siege'}
    armaments_dict["Reap What You Sow"] = { 'name':"Extinction Seeds", 'slot':'Armament:: Relic'}
    # armaments_dict[""] = { 'name':"Favor of Brough", 'slot':'Armament::Suport'}
    armaments_dict["Pyromaniac"] = { 'name':"Flamethrower", 'slot':'Armament::Siege'}
    # armaments_dict[""] = { 'name':"Font of Elation", 'slot':'Armament::Relic'}
    armaments_dict["Climb the Wall"] = { 'name':"Grappling Lines", 'slot':'Armament::Siege'}
    # armaments_dict[""] = { 'name':"Hallowed Ground", 'slot':'Armament::Support'}
    armaments_dict["Burning Bright"] = { 'name':"Holy Fire", 'slot':'Armament::Siege'}
    armaments_dict["Bargain"] = { 'name':"Infernal Agreement", 'slot':'Armament::Support'}
    armaments_dict["Gee Thanks"] = { 'name':"Insidious Gift", 'slot':'Armament::Siege'}
    armaments_dict["Fight As One"] = { 'name':"Iulian Foundation", 'slot':'Armament::Siege'}
    #armaments_dict[""] = { 'name':"Lightfoot Charm", 'slot':'Armament::Support'}
    # armaments_dict[""] = { 'name':"Martyr's Faith", 'slot':'Armament::Support'}
    armaments_dict["Witching Hour"] = { 'name':"Nightfall Orb", 'slot':'Armament::Relic'}
    armaments_dict["Terrible Presence"] = { 'name':"Overwhelming Aura", 'slot':'Armament::Support'}
    armaments_dict["Doorway"] = { 'name':"Portal Key", 'slot':'Armament::Relic'}
    armaments_dict["Ashes to Ashes"] = { 'name':"Sabirah's Ashes", 'slot':'Armament::Relic'}
    armaments_dict["Silver Bells"] = { 'name':"Saint's Chimes", 'slot':'Armament::Relic'}
    armaments_dict["Bad Crop"] = { 'name':"Shroud of Blight", 'slot':'Armament::Support'}
    armaments_dict["Sweet Ride"] = { 'name':"Siege Tower", 'slot':'Armament::Siege'}
    armaments_dict["Rain Of Fire"] = { 'name':"Skyfire Launcher", 'slot':'Armament::Relic'}
    armaments_dict["THIRTEENTH!"] = { 'name':"Standard of the 13th", 'slot':'Armament::Relic'}
    armaments_dict["Up and Over"] = { 'name':"Trebuchet", 'slot':'Armament::Siege'}
    # armaments_dict[""] = { 'name':"Turn Undead", 'slot':'Armament::Support'}
    armaments_dict["Corner of Your Eye"] = { 'name':"Whisperdark Torch", 'slot':'Armament::Relic'}
    # armaments_dict[""] = { 'name':"Withering Touch", 'slot':'Armament::Support'}

    return [generals_dict, mounts_dict, equipment_dict, troops_dict,
            legions_dict, enchantments_dict, engineering_dict, armaments_dict ]
