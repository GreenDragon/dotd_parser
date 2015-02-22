import yaml
import os

config = yaml.load(open(os.path.join(request.folder, 'private', 'apikey')).read())

connection = 'mysql://' + config['dbuser'] + ':' + config['dbpass'] + '@' + config['dbhost'] + '/' + config['db']

db = DAL(connection,pool_size=5,lazy_tables=True)

# UUID fields are generally 36 chars, DAL defaults to 128 chars
# Is the default Field type string when unspecified?

# uuid was 10 chars, uuid.uuid1() generates 36 chars
# Additionally, the previous uuid generator was making 12 chars

# Probably need some migrations here

db.define_table('raw_log',
                Field('data','text',default=''),
                Field('uuid',notnull=True,unique=True,length=128),
                Field('date','integer')
)

# UgUp doesn't provide proc_chance, proc_count,total_hits
# What is bdamageN, slot?
db.define_table('item',
                Field('name',unique=True,length=100),
                Field('proc_name'),
                Field('attack','integer'),
                Field('defense','integer'),
                Field('perception','integer'),
                Field('proc_chance','double'),
                Field('bdamage1','integer'),
                Field('bdamage2','integer'),
                Field('bdamage3','integer'),
                Field('bdamage4','integer'),
                Field('bdamage5','integer'),
                Field('bdamage6','integer'),
                Field('damage_cap','integer'),
                Field('slot'),
                Field('proc_count', 'bigint'),
                Field('total_hits','bigint')
)

# UgUp doesn't provide proc_chance, proc_count,total_hits
db.define_table('general',
                Field('name',unique=True,length=100),
                Field('proc_name'),
                Field('attack','integer'),
                Field('defense','integer'),
                Field('proc_chance','double'),
                Field('race'),
                Field('proc_count', 'bigint'),
                Field('total_hits','bigint')
)

# UgUp doesn't provide proc_chance, proc_count,total_hits
db.define_table('mount',
                Field('name',unique=True,length=100),
                Field('proc_name'),
                Field('attack','integer'),
                Field('defense','integer'),
                Field('perception','integer'),
                Field('proc_chance','double'),
                Field('proc_count', 'bigint'),
                Field('total_hits','bigint')
)

db.define_table('legion',
                Field('name',unique=True,length=100),
                Field('proc_name')
)

# Missing race
db.define_table('troop',
                Field('name',unique=True,length=100),
                Field('proc_name'),
                Field('attack','integer'),
                Field('defense','integer')
)

# Missing Enchantment proc_name mappings

db.raw_log.data.requires = IS_NOT_EMPTY()
