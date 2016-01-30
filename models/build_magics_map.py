def load_magics_map():
    magics_map = {}

    for row in db().select(db.dawn_magics.id, db.dawn_magics.name, db.dawn_magics.img_url):
        if len(row.name):
            if len(row.img_url):
                magics_map[row.id] = { 'name':row.name, 'img_url':row.img_url }

    return magics_map
