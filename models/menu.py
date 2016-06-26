# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

#response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
#                  _class="navbar-brand",_href="http://www.web2py.com/",
#                  _id="web2py-logo")
#response.title = request.application.replace('_',' ').title()

response.title = "Sentinel_V's DotD Raid Log Analyzer"
response.subtitle = response.title

## read more at http://dev.w3.org/html5/markup/meta.name.html

response.meta.author = 'Sentinel_V of Green Dragon Systems'
response.meta.description = 'Dawn of the Dragons Raid Log Analyzer. Hit your Raid and click on the "Copy entire raid log to clipboad" button, then paste the log into the textarea below.'
response.meta.keywords = 'Dawn of the Dragons, DotD, Raid Log Parser, Raid Log Analyzer, Log Parser, Log Analyzer, 5th Planet Games, Armorgames, Facebook, Kongregate, Newgrounds'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None


#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = False

PRODUCTION_MENU = True

def production_menu():
    response.menu += [
        ('DotD', False, None, [
            ('', False, A('Dawn of the Dragons: Forums',
             _href='http://www.dawnofthedragons.com/forums/forums/',
             _target='blank')),
            ('', False, A('Dawn of the Dragons: Game Page: Armor Games',
             _href='https://armorgames.com/dawn-of-the-dragons-game/13509',
             _target='blank')),
            # really, no TLS layer? Lazy gits!
            ('', False, A('Dawn of the Dragons: Game Page: Facebook',
             _href='http://www.dawnofthedragons.com/game/',
             _target='blank')),
            ('', False, A('Dawn of the Dragons: Game Page: Kongregate',
             _href='https://www.kongregate.com/games/5thPlanetGames/dawn-of-the-dragons',
             _target='blank')),
            ('', False, A('Dawn of the Dragons: Game Page: Newgrounds',
             _href='https://www.newgrounds.com/portal/view/609826',
             _target='blank')),
            ('', False, A('Dawn of the Dragons: Wiki',
             _href='http://dotd.wikia.com/wiki/Dawn_of_the_Dragons_Wiki',
             _target='blank')),
        ]),
        ('GitHub', False, None, [
            ('', False,
              A('GitHub: About/README',
              _href='https://github.com/GreenDragon/dotd_parser/blob/master/README.md',
              _target='blank')),
            ('', False,
              A('GitHub: Src/Bugs/Requests',
              _href='https://github.com/GreenDragon/dotd_parser',
              _target='blank')),
            ('', False,
              A('GitHub: Known Issues',
              _href='https://github.com/GreenDragon/dotd_parser/blob/master/KNOWN_ISSUES.md',
              _target='blank')),
            ('', False,
              A('GitHub: To Do',
              _href='https://github.com/GreenDragon/dotd_parser/blob/master/TO-DO.md',
              _target='blank')),
        ]),
    ]

if PRODUCTION_MENU: production_menu()

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    # useful links to internal and external resources
    response.menu += [
        (T('My Sites'), False, URL('admin', 'default', 'site')),
          (T('This App'), False, '#', [
              (T('Design'), False, URL('admin', 'default', 'design/%s' % app)),
              LI(_class="divider"),
              (T('Controller'), False,
               URL(
               'admin', 'default', 'edit/%s/controllers/%s.py' % (app, ctr))),
              (T('View'), False,
               URL(
               'admin', 'default', 'edit/%s/views/%s' % (app, response.view))),
              (T('DB Model'), False,
               URL(
               'admin', 'default', 'edit/%s/models/db.py' % app)),
              (T('Menu Model'), False,
               URL(
               'admin', 'default', 'edit/%s/models/menu.py' % app)),
              (T('Config.ini'), False,
               URL(
               'admin', 'default', 'edit/%s/private/appconfig.ini' % app)),
              (T('Layout'), False,
               URL(
               'admin', 'default', 'edit/%s/views/layout.html' % app)),
              (T('Stylesheet'), False,
               URL(
               'admin', 'default', 'edit/%s/static/css/web2py-bootstrap3.css' % app)),
              (T('Database'), False, URL(app, 'appadmin', 'index')),
              (T('Errors'), False, URL(
               'admin', 'default', 'errors/' + app)),
              (T('About'), False, URL(
               'admin', 'default', 'about/' + app)),
              ]),
          ('web2py.com', False, '#', [
             (T('Download'), False,
              'http://www.web2py.com/examples/default/download'),
             (T('Support'), False,
              'http://www.web2py.com/examples/default/support'),
             (T('Demo'), False, 'http://web2py.com/demo_admin'),
             (T('Quick Examples'), False,
              'http://web2py.com/examples/default/examples'),
             (T('FAQ'), False, 'http://web2py.com/AlterEgo'),
             (T('Videos'), False,
              'http://www.web2py.com/examples/default/videos/'),
             (T('Free Applications'),
              False, 'http://web2py.com/appliances'),
             (T('Plugins'), False, 'http://web2py.com/plugins'),
             (T('Recipes'), False, 'http://web2pyslices.com/'),
             ]),
          (T('Documentation'), False, '#', [
             (T('Online book'), False, 'http://www.web2py.com/book'),
             LI(_class="divider"),
             (T('Preface'), False,
              'http://www.web2py.com/book/default/chapter/00'),
             (T('Introduction'), False,
              'http://www.web2py.com/book/default/chapter/01'),
             (T('Python'), False,
              'http://www.web2py.com/book/default/chapter/02'),
             (T('Overview'), False,
              'http://www.web2py.com/book/default/chapter/03'),
             (T('The Core'), False,
              'http://www.web2py.com/book/default/chapter/04'),
             (T('The Views'), False,
              'http://www.web2py.com/book/default/chapter/05'),
             (T('Database'), False,
              'http://www.web2py.com/book/default/chapter/06'),
             (T('Forms and Validators'), False,
              'http://www.web2py.com/book/default/chapter/07'),
             (T('Email and SMS'), False,
              'http://www.web2py.com/book/default/chapter/08'),
             (T('Access Control'), False,
              'http://www.web2py.com/book/default/chapter/09'),
             (T('Services'), False,
              'http://www.web2py.com/book/default/chapter/10'),
             (T('Ajax Recipes'), False,
              'http://www.web2py.com/book/default/chapter/11'),
             (T('Components and Plugins'), False,
              'http://www.web2py.com/book/default/chapter/12'),
             (T('Deployment Recipes'), False,
              'http://www.web2py.com/book/default/chapter/13'),
             (T('Other Recipes'), False,
              'http://www.web2py.com/book/default/chapter/14'),
             (T('Helping web2py'), False,
              'http://www.web2py.com/book/default/chapter/15'),
             (T("Buy web2py's book"), False,
              'http://stores.lulu.com/web2py'),
             ]),
          (T('Community'), False, None, [
             (T('Groups'), False,
              'http://www.web2py.com/examples/default/usergroups'),
              (T('Twitter'), False, 'http://twitter.com/web2py'),
              (T('Live Chat'), False,
               'http://webchat.freenode.net/?channels=web2py'),
              ]),
        ]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu() 
