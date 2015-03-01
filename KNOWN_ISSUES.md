* [Application] Invalid log files cause stack traces
  * enter garbage to the web form
  * biggest_hit = max(hit_list, key=hit_list.get)
    * ValueError: max() arg is an empty sequence
* [Production] Debian: web2py needs to run with dedicated user ( www-data )
* [Production] Debian: modsecurity with a default config kills large posts
  * wsgi crashes with 400 error
  * raise HTTP(400, "Bad Request - HTTP body is incomplete")
  * Need to tweak  /etc/modsecurity/
