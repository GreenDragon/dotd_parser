def load_proc_to_names():
    generals_dict = {}
    mounts_dict = {}
    equipment_dict = {}
    troops_dict = {}
    legions_dict = {}
    enchantments_dict = {}
    engineering_dict = {}

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

    return [generals_dict, mounts_dict, equipment_dict, troops_dict,
            legions_dict, enchantments_dict, engineering_dict ]
