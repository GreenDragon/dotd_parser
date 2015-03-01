#
# Currently we don't do multi-lingual support
# 
# See router.example.py for language customization hints
#
# To INSTALL: copy this file to youe base web2py installation: 
#    ./web2py/routes.py 
# Then restart your server deployment ( web2py, apache w/mod_wsgi )
#
routers = dict(
    BASE = dict(default_application='dotd_parser'),
)
