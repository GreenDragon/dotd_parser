def form():
    db.raw_log.uuid.default = uuid_generator()
    db.raw_log.date.default = dbdate()

    # don't display form items that are part of table, but not facing end user
    db.raw_log.uuid.readable = db.raw_log.uuid.writable = False
    db.raw_log.date.readable = db.raw_log.date.writable = False

    #if form.accepted:
    #    redirect(URL('dotd', 'parsed', args=db.raw_log.uuid.default))
    form=FORM(TABLE(TR("Enter yer Log Human:",INPUT(_type="text",_name="log_data",requires=IS_NOT_EMPTY())),
                    TR("",INPUT(_type="submit",_value="SUBMIT"))))
    if form.accepts(request,session):
        response.flash="form accepted"
    elif form.errors:
        response.flash="form is invalid"
    else
        response.flash="please fill in the form"

    return dict(form=form,vars=form.vars)


def parsed():
    if request.args:
        uuid = request.args[0]
        rows = db(db.raw_log.uuid == uuid).select()
        if len(rows) == 0:
            redirect(URL('form'))
        for row in rows:
            experience, obtained_items, proc_items, found_items, log_file, max_hit, hit_list = parser(row.data)
            # hit_list=parser(row.data)
        return locals()
    else:
        redirect(URL('form'))
