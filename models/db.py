# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


# driver_args was required by my dev environment
# Mac OS X 10.9.5, MySQL CE 5.6.23, MacPorts Python 2.7.9_0+ucs4
# Otherwise, MacPorts Python wants to bind to macports mariadb buildout
#   driver_args={'unix_socket':'/tmp/mysql.sock'},

#if not request.env.web2py_runtime_gae:
#    ## if NOT running on Google App Engine use SQLite or other DB

# db = DAL(connection, pool_size=5, lazy_tables=True)
db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int))

#else:
#    ## connect to Google BigTable (optional 'google:datastore://namespace')
#    db = DAL('google:datastore+ndb')
#    ## store sessions and tickets there
#    session.connect(request, response, db=db)
#    ## or store session in Memcache, Redis, etc.
#    ## from gluon.contrib.memdb import MEMDB
#    ## from google.appengine.api.memcache import Client
#    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []

## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.sender')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

# disable registration for now
auth.settings.actions_disabled.append('register')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

# JSON UgUp API fields def and unique are problematic to python and mysql
# Length for uuid field is required for MySQL InnoDB tables
# DAL -> MySQL does boolean fields as char(1)

db.define_table('logs',
                Field('uuid', 'string', length=48, unique=True, readable=False, writable=False),
                Field('date', 'datetime', readable=False, writable=False, default=request.now),
                Field('data', 'text', requires=IS_NOT_EMPTY()),
)

# All following tables propagated by cron utilities...

db.define_table('dawn_enchantments',
                Field('name', 'string'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
)

#

db.define_table('suns_enchantments',
                Field('name', 'string'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
)

#

db.define_table('dawn_equipment',
                Field('name', 'string'),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('perception', 'integer'),
                Field('rarity', 'integer'),
                Field('value_gold', 'integer'),
                Field('value_credits', 'integer'),
                Field('value_gtoken', 'integer'),
                Field('questReq', 'integer'),
                Field('isUnique', 'integer'),
                Field('canEnchant', 'integer'),
                Field('equipType', 'integer'),
                Field('hlt', 'integer'),
                Field('eng', 'integer'),
                Field('sta', 'integer'),
                Field('hnr', 'integer'),
                Field('atk', 'integer'),
                Field('defn', 'integer'),
                Field('power', 'integer'),
                Field('dmg', 'integer'),
                Field('deflect', 'integer'),
                Field('lore', 'text'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
)

db.define_table('suns_equipment',
                Field('name', 'string'),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('perception', 'integer'),
                Field('rarity', 'integer'),
                Field('value_gold', 'integer'),
                Field('value_credits', 'integer'),
                Field('value_gtoken', 'integer'),
                Field('questReq', 'integer'),
                Field('isUnique', 'integer'),
                Field('canEnchant', 'integer'),
                Field('equipType', 'integer'),
                Field('hlt', 'integer'),
                Field('eng', 'integer'),
                Field('sta', 'integer'),
                Field('hnr', 'integer'),
                Field('atk', 'integer'),
                Field('defn', 'integer'),
                Field('power', 'integer'),
                Field('dmg', 'integer'),
                Field('deflect', 'integer'),
                Field('lore', 'text'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
)

#

db.define_table('dawn_generals',
                Field('name', 'string'),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('race', 'integer'),
                Field('role', 'integer'),
                Field('rarity', 'integer'),
                Field('value_gold', 'integer'),
                Field('value_credits', 'integer'),
                Field('questReq', 'integer'),
                Field('source', 'integer'),
                Field('buffType', 'integer'),
                Field('lore', 'text'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
)

db.define_table('suns_generals',
                Field('name', 'string'),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('race', 'integer'),
                Field('role', 'integer'),
                Field('rarity', 'integer'),
                Field('value_gold', 'integer'),
                Field('value_credits', 'integer'),
                Field('questReq', 'integer'),
                Field('source', 'integer'),
                Field('buffType', 'integer'),
                Field('lore', 'text'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
)

#

db.define_table('dawn_legions',
                Field('name', 'string'),
                Field('num_gen', 'integer'),
                Field('num_trp', 'integer'),
                Field('bonus', 'integer'),
                Field('bonusSpecial', 'integer'),
                Field('bonusText', 'string'),
                Field('rarity', 'integer'),
                Field('value_gold', 'integer'),
                Field('value_credits', 'integer'),
                Field('canPurchase', 'integer'),
                Field('questReq', 'integer'),
                Field('lore', 'text'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
                Field('specification', 'string'),
                Field('general_format', 'json'),
                Field('troop_format', 'json'),
)

db.define_table('suns_legions',
                Field('name', 'string'),
                Field('num_gen', 'integer'),
                Field('num_trp', 'integer'),
                Field('bonus', 'integer'),
                Field('bonusSpecial', 'integer'),
                Field('bonusText', 'string'),
                Field('rarity', 'integer'),
                Field('value_gold', 'integer'),
                Field('value_credits', 'integer'),
                Field('canPurchase', 'integer'),
                Field('questReq', 'integer'),
                Field('lore', 'text'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
                Field('specification', 'string'),
                Field('general_format', 'json'),
                Field('troop_format', 'json'),
)

#

db.define_table('dawn_mounts',
                Field('name', 'string'),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('perception', 'integer'),
                Field('rarity', 'integer'),
                Field('value_gold', 'integer'),
                Field('value_credits', 'integer'),
                Field('questReq', 'integer'),
                Field('isUnique', 'integer'),
                Field('hlt', 'integer'),
                Field('eng', 'integer'),
                Field('sta', 'integer'),
                Field('hnr', 'integer'),
                Field('atk', 'integer'),
                Field('defn', 'integer'),
                Field('power', 'integer'),
                Field('dmg', 'integer'),
                Field('deflect', 'integer'),
                Field('lore', 'text'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
)

db.define_table('suns_mounts',
                Field('name', 'string'),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('perception', 'integer'),
                Field('rarity', 'integer'),
                Field('value_gold', 'integer'),
                Field('value_credits', 'integer'),
                Field('questReq', 'integer'),
                Field('isUnique', 'integer'),
                Field('hlt', 'integer'),
                Field('eng', 'integer'),
                Field('sta', 'integer'),
                Field('hnr', 'integer'),
                Field('atk', 'integer'),
                Field('defn', 'integer'),
                Field('power', 'integer'),
                Field('dmg', 'integer'),
                Field('deflect', 'integer'),
                Field('lore', 'text'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
)

#

db.define_table('dawn_troops',
                Field('name', 'string'),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('race', 'integer'),
                Field('role', 'integer'),
                Field('rarity', 'integer'),
                Field('value_gold', 'integer'),
                Field('value_credits', 'integer'),
                Field('canPurchase', 'integer'),
                Field('questReq', 'integer'),
                Field('source', 'integer'),
                Field('buffType', 'integer'),
                Field('lore', 'text'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
)

db.define_table('suns_troops',
                Field('name', 'string'),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('race', 'integer'),
                Field('role', 'integer'),
                Field('rarity', 'integer'),
                Field('value_gold', 'integer'),
                Field('value_credits', 'integer'),
                Field('canPurchase', 'integer'),
                Field('questReq', 'integer'),
                Field('source', 'integer'),
                Field('buffType', 'integer'),
                Field('lore', 'text'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
)

# Unique to suns

db.define_table('suns_engineering',
                Field('name', 'string'),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('engineering', 'integer'),
                Field('value_credits', 'integer'),
                Field('isUnique', 'integer'),
                Field('lore', 'text'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
                Field('bonus', 'json'),
)

# DotD World Raids

db.define_table('dawn_shared_raids',
                Field('create_time', 'datetime'),
                Field('platform', 'string'),
                Field('link_name', 'string'),
                Field('raid_id', 'integer'),
                Field('difficulty', 'integer'),
                Field('raid_boss', 'string'),
                Field('raid_hash', 'string'),
                Field('serverid', 'integer'),
)

# LoTS World Raids

db.define_table('suns_shared_raids',
                Field('create_time', 'datetime'),
                Field('platform', 'string'),
                Field('link_name', 'string'),
                Field('raid_id', 'integer'),
                Field('difficulty', 'integer'),
                Field('raid_boss', 'string'),
                Field('raid_hash', 'string'),
                Field('serverid', 'integer'),
)

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
