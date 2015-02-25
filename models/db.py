# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

import yaml
import os

config = yaml.load(open(os.path.join(request.folder, 'private', 'apikey')).read())

connection = 'mysql://' + config['dbuser'] + ':' + config['dbpass'] + '@' + config['dbhost'] + '/' + config['db']

# driver_args is required by my dev environment
# Mac OS X 10.9.5, MySQL CE 5.6.23, MacPorts Python 2.7.9_0+ucs4
# Otherwise, MacPorts Python wants to bind to macports mariadb buildout
#   driver_args={'unix_socket':'/tmp/mysql.sock'},

db = DAL(connection, pool_size=5)

# while lazy_tables is good for production, it's a PITA for development
# lazy_tables=True

#if not request.env.web2py_runtime_gae:
#    ## if NOT running on Google App Engine use SQLite or other DB
#    # db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'])
#    db = DAL('mysql://root:password@localhost/test_dotd_parser',
#             driver_args={'unix_socket':'/tmp/mysql.sock'},
#             pool_size=5,
#             lazy_tables=True)
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
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
# from gluon.contrib.login_methods.janrain_account import use_janrain
# use_janrain(auth, filename='private/janrain.key')

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

db.define_table('raw_log',
                Field('uuid', 'string', length=48, notnull=True, unique=True),
                Field('date', 'datetime'),
                Field('data', 'text'),
)

db.define_table('enchantments',
                Field('name', 'string'),
                Field('proc_name', 'string'),
                Field('proc_desc', 'text'),
)

db.define_table('equipment',
                Field('name', 'string'),
                Field('attack', 'integer'),
                Field('defense', 'integer'),
                Field('perception', 'integer'),
                Field('rarity', 'integer'),
                Field('value_gold', 'integer'),
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

db.define_table('generals',
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

db.define_table('legions',
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

db.define_table('mounts',
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

db.define_table('troops',
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


## after defining tables, uncomment below to enable auditing
# Maybe not quite yet, I don't think we need to track all record changes yet
# auth.enable_record_versioning(db)

# From previous db.py file, not sure what this accomplishes yet IRT Lazy Loading
# Or some sort of form validation?

db.raw_log.data.requires = IS_NOT_EMPTY()
