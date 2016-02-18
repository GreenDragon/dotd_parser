# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    redirect(URL('form'))


def form():
    form = SQLFORM(db.logs, labels={'data':''}, formstyle='divs')
    form.vars.uuid = uuid_generator()

    if form.process().accepted:
        redirect(URL('parsed', args=form.vars.uuid))
    elif form.errors:
        response.flash = T("Form had errors. Did you forget to paste some data?")
    return dict(form=form)


def parsed():
    if request.args:
        uuid = request.args[0]
        row = db(db.logs.uuid==uuid).select()
        # There can only be one
        if len(row) == 0:
            session.flash = T("UUID not found or was purged from the DB")
            redirect(URL('form'))
        # We should never get here since uuid is a unique row in the table
        if len(row) > 1:
            session.flash = T("Something wicked this way went")
            redirect(URL('form'))
        # Leroy Jenkins! Let's do this!
        experience, obtained_items, proc_items, found_items, log_file, max_hit, hit_list, restored_items, \
           affected_items, created_items, rant_items, magic_items, triggered_items, log_suns_mode, \
           multi_procs_found, multi_proc_items = parser(row[0].data)

        return locals()
    else:
        session.flash = T("Expected a known or valid UUID")
        redirect(URL('form'))


def armorgames_raids_dotd_roland():
    rows = db((db.dawn_shared_raids_armor_s1.iscomplete=='0') & (db.dawn_shared_raids_armor_s1.update_time!=None)).select(orderby=~db.dawn_shared_raids_armor_s1.create_time,limitby=(0,500))
    magics_map = load_magics_map()
    return locals()


def armorgames_raids_dotd_kasan_world():
    rows = db((db.dawn_shared_raids_armor_s2.iscomplete=='0') & (db.dawn_shared_raids_armor_s2.update_time!=None)).select(orderby=~db.dawn_shared_raids_armor_s2.create_time,limitby=(0,500))
    magics_map = load_magics_map()
    return locals()


def facebook_raids_dotd_solus():
    rows = db((db.dawn_shared_raids_fb_s1.iscomplete=='0') & (db.dawn_shared_raids_fb_s1.update_time!=None)).select(orderby=~db.dawn_shared_raids_fb_s1.create_time,limitby=(0,500))
    magics_map = load_magics_map()
    return locals()


def facebook_raids_dotd_kasan_world():
    rows = db((db.dawn_shared_raids_fb_s2.iscomplete=='0') & (db.dawn_shared_raids_fb_s2.update_time!=None)).select(orderby=~db.dawn_shared_raids_fb_s2.create_time,limitby=(0,500))
    magics_map = load_magics_map()
    return locals()


def kongregate_raids_dotd_elyssa():
    rows = db((db.dawn_shared_raids_kong_s1.iscomplete=='0') & (db.dawn_shared_raids_kong_s1.update_time!=None)).select(orderby=~db.dawn_shared_raids_kong_s1.create_time,limitby=(0,500))
    magics_map = load_magics_map()
    return locals()


def kongregate_raids_dotd_kasan_world():
    rows = db((db.dawn_shared_raids_kong_s2.iscomplete=='0') & (db.dawn_shared_raids_kong_s2.update_time!=None)).select(orderby=~db.dawn_shared_raids_kong_s2.create_time,limitby=(0,500))
    magics_map = load_magics_map()
    return locals()


def newgrounds_raids_dotd_roland():
    rows = db((db.dawn_shared_raids_ng_s1.iscomplete=='0') & (db.dawn_shared_raids_ng_s1.update_time!=None)).select(orderby=~db.dawn_shared_raids_ng_s1.create_time,limitby=(0,500))
    magics_map = load_magics_map()
    return locals()


def newgrounds_raids_dotd_kasan_world():
    rows = db((db.dawn_shared_raids_ng_s2.iscomplete=='0') & (db.dawn_shared_raids_ng_s2.update_time!=None)).select(orderby=~db.dawn_shared_raids_ng_s2.create_time,limitby=(0,500))
    magics_map = load_magics_map()
    return locals()


def facebook_raids_lots():
    rows = db((db.suns_shared_raids.iscomplete=='0') & (db.suns_shared_raids.update_time!=None)).select(orderby=~db.suns_shared_raids.create_time,limitby=(0,500))
    tactics_map = load_tactics_map()
    return locals()

def armorgames_raids_lots():
    rows = db((db.suns_shared_raids_armor.iscomplete=='0') & (db.suns_shared_raids_armor.update_time!=None)).select(orderby=~db.suns_shared_raids_armor.create_time,limitby=(0,500))
    tactics_map = load_tactics_map()
    return locals()

def kongregate_raids_lots():
    rows = db((db.suns_shared_raids_kong.iscomplete=='0') & (db.suns_shared_raids_kong.update_time!=None)).select(orderby=~db.suns_shared_raids_kong.create_time,limitby=(0,500))
    tactics_map = load_tactics_map()
    return locals()

def newgrounds_raids_lots():
    rows = db((db.suns_shared_raids_ng.iscomplete=='0') & (db.suns_shared_raids_ng.update_time!=None)).select(orderby=~db.suns_shared_raids_ng.create_time,limitby=(0,500))
    tactics_map = load_tactics_map()
    return locals()


def user():
    redirect(URL('form'))
#    """
#    exposes:
#    http://..../[app]/default/user/login
#    http://..../[app]/default/user/logout
#    http://..../[app]/default/user/register
#    http://..../[app]/default/user/profile
#    http://..../[app]/default/user/retrieve_password
#    http://..../[app]/default/user/change_password
#    http://..../[app]/default/user/manage_users (requires membership in
#    use @auth.requires_login()
#        @auth.requires_membership('group name')
#        @auth.requires_permission('read','table name',record_id)
#    to decorate functions that need access control
#    """
#    return dict(form=auth())


#@cache.action()
#def download():
#    """
#    allows downloading of uploaded files
#    http://..../[app]/default/download/[filename]
#    """
#    return response.download(request, db)


#def call():
#    """
#    exposes services. for example:
#    http://..../[app]/default/call/jsonrpc
#    decorate with @services.jsonrpc the functions to expose
#    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
#    """
#    return service()


