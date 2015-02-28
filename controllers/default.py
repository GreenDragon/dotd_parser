# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - api is an example of Hypermedia API support and access control
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
    form = SQLFORM(db.raw_log, labels={'data':''}, formstyle='divs')
    form.vars.uuid = uuid_generator()

    if form.process().accepted:
        # session.flash = T("Form Accepted")
        redirect(URL('parsed', args=form.vars.uuid))
    elif form.errors:
        response.flash = T("Form had errors. Did you forget to paste some data?")
    #else:
    #    response.flash = T("Please fill out the form")
    return dict(form=form)

def parsed():
    if request.args:
        uuid = request.args[0]
        row = db(db.raw_log.uuid==uuid).select()
        if len(row) == 0:
            session.flash = T("UUID not found or was purged from the DB")
            redirect(URL('form'))
        # We should never get here since uuid is a unique row in the table
        if len(row) > 1:
            session.flash = T("Something wicked this way went")
            redirect(URL('form'))
        # Leroy Jenkins! Let's do this!
        experience, obtained_items, proc_items, found_items, log_file, max_hit, hit_list=parser(row[0].data)
        return locals()
    else:
        session.flash = T("Expected a known or valid UUID")
        redirect(URL('form'))


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


#@auth.requires_login()
#def api():
#    """
#    this is example of API with access control
#    WEB2PY provides Hypermedia API (Collection+JSON) Experimental
#    """
#    from gluon.contrib.hypermedia import Collection
#    rules = {
#        '<tablename>': {'GET':{},'POST':{},'PUT':{},'DELETE':{}},
#        }
#    return Collection(db).process(request,response,rules)
