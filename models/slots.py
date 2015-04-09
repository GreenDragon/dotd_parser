def get_dawn_equip_name(x):
    equipment= {  1: 'Main Hand',
                  2: 'Off Hand',
                  3: 'Helm',
                  4: 'Chest',
                  5: 'Gloves',
                  6: 'Pants',
                  7: 'Boots',
                  8: 'Ring',
                  9: 'Shield',
                  10: 'Neck' }

    if type(x) in [ type(0), type(0L) ]:
        if x in range(1,11):
            return equipment[x]
        else:
            return 'Equipment'
    else:
        return 'Equipment'

def get_sun_equip_name(x):
    equipment = {  1: 'Main Hand',
                   2: 'Off Hand',
                   3: 'Helmet',
                   4: 'Chest',
                   5: 'Gloves',
                   6: 'Pants',
                   7: 'Boots',
                   8: 'Trinket',
                   9: 'Shield' }

    if type(x) in [ type(0), type(0L) ]:
        if x in range(1,10):
            return equipment[x]
        else:
            return 'Equipment'
    else:
        return 'Equipment'


def get_suns_engineer_name(x):
    engineering = { 1: 'Eng: AI',
                    2: 'Eng: Weapons',
                    3: 'Eng: Modules'}

    if type(x) in [ type(0), type(0L) ]:
        if x in range(1,4):
            return engineering[x]
        else:
            return 'Engineering'
    else:
        return 'Engineering'

