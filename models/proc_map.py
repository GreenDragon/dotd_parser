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
    armaments_dict["Tiny Bubbles"] = {'name': "Acid", 'slot': 'Armament::Siege'}
    armaments_dict["The Ride"] = {'name': "Air Support", 'slot': 'Armament::Siege'}
    armaments_dict["Opposite Day"] = {'name': "Amulet of Inversion", 'slot': 'Armament::Relic'}
    armaments_dict["Stay"] = { 'name':"Anchor of the Grimval", 'slot':'Armament::Relic'}
    # armaments_dict[""] = { 'name':"Armorskin Charm", 'slot':'Armament::Support'}
    armaments_dict["Alone Time"] = { 'name':"Aura of Isolation", 'slot':'Armament::Support'}
    armaments_dict["Scented"] = { 'name':"Azar's Candle", 'slot':'Armament::Relic'}
    armaments_dict["Arrow'd"] = { 'name':"Ballista", 'slot':'Armament::Siege'}
    armaments_dict["Who's There"] = { 'name':"Battering Ram", 'slot':'Armament::Siege'}
    armaments_dict["Scream and Shout"] = { 'name':"Berserker's Horn", 'slot':'Armament::Relic'}
    armaments_dict["BOOM"] = { 'name':"Black Powder", 'slot':'Armament::Siege'}
    armaments_dict["Unsinkable"] = {'name': "Blessing of Bouyancy", 'slot': 'Armament::Support'}
    # armaments_dict[""] = { 'name':"Blessing of Karuss", 'slot':'Armament::Support'}
    armaments_dict["Memory of Melops"] = {'name': "Callissa's Sail", 'slot': 'Armament::Relic'}
    armaments_dict["Heads Up"] = { 'name':"Catapult", 'slot':'Armament::Siege'}
    armaments_dict["Advanced Warfare"] = {'name': "Catapult Catapult", 'slot': 'Armament::Siege'}
    armaments_dict["Fervor"] = { 'name':"Cermarina's Blade", 'slot':'Armament::Relic'}
    armaments_dict["The Sound of War"] = {'name': "Conquest Drums", 'slot': 'Armament::Relic'}
    armaments_dict["I'm Back"] = { 'name':"Curse of Returning", 'slot':'Armament::Support'}
    # armaments_dict[""] = { 'name':"Decoys", 'slot':'Armament::Siege'}
    armaments_dict["Biological Warfare"] = { 'name':"Diseased Corpses", 'slot':'Armament::Siege'}
    armaments_dict["Ultimate Power, Possibly"] = { 'name':"Evelyn's Urn", 'slot':'Armament::Relic'}
    armaments_dict["Reap What You Sow"] = { 'name':"Extinction Seeds", 'slot':'Armament:: Relic'}
    # armaments_dict[""] = { 'name':"Favor of Brough", 'slot':'Armament::Suport'}
    armaments_dict["Pyromaniac"] = { 'name':"Flamethrower", 'slot':'Armament::Siege'}
    # armaments_dict[""] = { 'name':"Font of Elation", 'slot':'Armament::Relic'}
    armaments_dict["Climb the Wall"] = { 'name':"Grappling Lines", 'slot':'Armament::Siege'}
    # armaments_dict[""] = { 'name':"Hallowed Ground", 'slot':'Armament::Support'}
    armaments_dict["Guidance"] = { 'name':"Hero's Teachings", 'slot':'Armament::Support'}
    armaments_dict["Swarm"] = { 'name':"Hive Mind Hex", 'slot':'Armament::Support'}
    armaments_dict["Burning Bright"] = { 'name':"Holy Fire", 'slot':'Armament::Siege'}
    armaments_dict["And Sinker"] = { 'name':"Hook Lines", 'slot':'Armament::Siege'}
    armaments_dict["Bargain"] = { 'name':"Infernal Agreement", 'slot':'Armament::Support'}
    armaments_dict["Gee Thanks"] = { 'name':"Insidious Gift", 'slot':'Armament::Siege'}
    armaments_dict["Cold Iron"] = {'name': "Iron Barricade", 'slot': 'Armament::Siege'}
    armaments_dict["Fight As One"] = { 'name':"Iulian Foundation", 'slot':'Armament::Siege'}
    armaments_dict["Lay to Rest"] = {'name': "Last Rites", 'slot': 'Armament::Support'}
    armaments_dict["War of Angels"] = {'name': "Lerilith's Cry", 'slot': 'Armament::Support'}
    # armaments_dict[""] = { 'name':"Lightfoot Charm", 'slot':'Armament::Support'}
    armaments_dict["Give It"] = {'name': "Magic Magnet", 'slot': 'Armament::Relic'}
    # armaments_dict[""] = { 'name':"Martyr's Faith", 'slot':'Armament::Support'}
    # armaments_dict[""] = { 'name':"Men of Kruna", 'slot':'Armament::Support'}
    armaments_dict["Someone Your Own Size"] = {'name': "Might of Terracles", 'slot': 'Armament::Support'}
    armaments_dict["Witching Hour"] = { 'name':"Nightfall Orb", 'slot':'Armament::Relic'}
    armaments_dict["Word is Bond"] = {'name': "Oath", 'slot': 'Armament::Support'}
    armaments_dict["Terrible Presence"] = { 'name':"Overwhelming Aura", 'slot':'Armament::Support'}
    armaments_dict["One False Step"] = {'name': "Pit Trap", 'slot': 'Armament::Siege'}
    armaments_dict["Corrupt Water"] = {'name': "Poison", 'slot': 'Armament::Siege'}
    armaments_dict["Doorway"] = { 'name':"Portal Key", 'slot':'Armament::Relic'}
    #armaments_dict[""] = { 'name':"Ramis' Retriever", 'slot':'Armament::Relic'}
    armaments_dict["Ashes to Ashes"] = { 'name':"Sabirah's Ashes", 'slot':'Armament::Relic'}
    armaments_dict["Silver Bells"] = { 'name':"Saint's Chimes", 'slot':'Armament::Relic'}
    armaments_dict["Bad Crop"] = { 'name':"Shroud of Blight", 'slot':'Armament::Support'}
    armaments_dict["Sweet Ride"] = { 'name':"Siege Tower", 'slot':'Armament::Siege'}
    armaments_dict["Rain Of Fire"] = { 'name':"Skyfire Launcher", 'slot':'Armament::Relic'}
    armaments_dict["Flap in the Night"] = { 'name':"Smoke Screen", 'slot':'Armament::Siege'}
    armaments_dict["THIRTEENTH!"] = { 'name':"Standard of the 13th", 'slot':'Armament::Relic'}
    armaments_dict["Consume All"] = { 'name':"Swarmcaller Staff", 'slot':'Armament::Relic'}
    armaments_dict["Ground Supremacy"] = {'name': "Tactical Map", 'slot': 'Armament::Siege'}
    armaments_dict["Catchy Tune"] = {'name': "The Pan Pipe of Liven", 'slot': 'Armament::Relic'}
    armaments_dict["Half Shell of a Hero"] = {'name': "The Shell of Solus", 'slot': 'Armament::Relic'}
    armaments_dict["Up and Over"] = { 'name':"Trebuchet", 'slot':'Armament::Siege'}
    # armaments_dict[""] = { 'name':"Turn Undead", 'slot':'Armament::Support'}
    # armaments_dict[""] = { 'name':"Valkyries's Blessing", 'slot':'Armament::Support'}
    # armaments_dict[""] = { 'name':"Warrior's Prayer", 'slot':'Armament::Support'}
    armaments_dict["Gillyweed"] = { 'name':"Waterbreathing Charm", 'slot':'Armament::Support'}
    armaments_dict["Trouble the Water"] = {'name': "Waterwalking Charm", 'slot': 'Armament::Support'}
    armaments_dict["Corner of Your Eye"] = { 'name':"Whisperdark Torch", 'slot':'Armament::Relic'}
    # armaments_dict[""] = { 'name':"Withering Touch", 'slot':'Armament::Support'}

    return [generals_dict, mounts_dict, equipment_dict, troops_dict,
            legions_dict, enchantments_dict, engineering_dict, armaments_dict ]
