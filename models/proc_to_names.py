def load_proc_to_names():
    generals_translation = {}
    mounts_translation = {}
    equipment_translation = {}
    troops_translation = {}
    legions_translation = {}

    gen_dawn_list = db().select(db.dawn_generals.name, db.dawn_generals.proc_name)
    mount_dawn_list = db().select(db.dawn_mounts.name, db.dawn_mounts.proc_name)
    equip_dawn_list = db().select(db.dawn_equipment.name, db.dawn_equipment.proc_name)
    troop_dawn_list = db().select(db.dawn_troops.name, db.dawn_troops.proc_name)
    legion_dawn_list = db().select(db.dawn_legions.name, db.dawn_legions.proc_name)

    gen_suns_list = db().select(db.suns_generals.name, db.suns_generals.proc_name)
    mount_suns_list = db().select(db.suns_mounts.name, db.suns_mounts.proc_name)
    equip_suns_list = db().select(db.suns_equipment.name, db.suns_equipment.proc_name)
    troop_suns_list = db().select(db.suns_troops.name, db.suns_troops.proc_name)
    legion_suns_list = db().select(db.suns_legions.name, db.suns_legions.proc_name)

    for row in gen_dawn_list:
        generals_translation[row.proc_name] = row.name

    for row in gen_suns_list:
        generals_translation[row.proc_name] = row.name

    for row in mount_dawn_list:
        mounts_translation[row.proc_name] = row.name

    for row in mount_suns_list:
        mounts_translation[row.proc_name] = row.name

    for row in equip_dawn_list:
        equipment_translation[row.proc_name] = row.name

    for row in equip_suns_list:
        equipment_translation[row.proc_name] = row.name

    for row in troop_dawn_list:
        troops_translation[row.proc_name] = row.name

    for row in troop_suns_list:
        troops_translation[row.proc_name] = row.name

    for row in legion_dawn_list:
        legions_translation[row.proc_name] = row.name

    for row in legion_suns_list:
        legions_translation[row.proc_name] = row.name

    return [generals_translation, mounts_translation,
            equipment_translation, troops_translation, legions_translation]
