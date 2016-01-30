def load_tactics_map():
    tactics_map = {}

    for row in db().select(db.suns_magics.id, db.suns_magics.name, db.suns_magics.img_url):
        if len(row.name):
            if len(row.img_url):
                tactics_map[row.id] = { 'name':row.name, 'img_url':row.img_url }

    return tactics_map
