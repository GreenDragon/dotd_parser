Dawn of the Dragons Log Parser
===

### About:

A Web2py web application to parse 5th Planet Games raid logs into useful statistical information.

### Development/Testing Environment:

    * Mac OS X 10.10.5
        * web2py Version Version 2.10.3-stable+timestamp.2015.04.02.21.42.07
        * MySQL Community Edition
            * MySQL 5.7.9, for osx10.10 (x86_64)
        * Python 2.7.10 via MacPorts
            * python27 @2.7.10_3
            * py-mysql @1.2.3_1 (active)
                * py27-mysql @1.2.3_1+mariadb55 (active)
            * py-requests @2.8.1_0 (active)
                * py27-requests @2.8.1_0 (active)
            * py-yaml @3.11_0 (active)
                * py27-yaml @3.11_0 (active)

### Production Environment:
    
    * Debian 8.0 ( https://www.linode.com/ )
        * web2py Version 2.10.3-stable+timestamp.2015.04.02.21.42.07
        * MariaDB 
            * mariadb-server                       10.0.22-0+deb8u1
        * Python 2.7
            * python2.7                            2.7.9-2
            * python-mysqldb                       1.2.3-2.1
            * python-requests                      2.4.3-6
            * python-yaml                          3.11-2
        * Apache 2.4.x
            * apache2                              2.4.10-10+deb8u3
            * libapache2-mod-wsgi                  4.3.0-1

### Requirements:

Prerequisites ( Unix only ):

    * Python 2.7.x
        * python-mysqldb  >= 1.2.3
        * python-requests >= 0.12.1
    * MySQL 5.5 or newer ( or equivalent MariaDB )
    * web2py >= 2.10.3 
    * Apache 2.2 or newer + mod-wsgi 3.3 or newer
    * UgUp API Key from 5th Planet games: http://bit.ly/1jSdVoQ

### Setup:

Download web2py_src.zip from http://web2py.com/init/default/download and extract:
```
    $ cd <development_directory>
    $ mv ~/Downloads/web2py_src.zip .
    $ unzip -a web2py_src.zip
```

Clone the application repository from github:
```
    $ cd <development_directory>/web2py/applications
    $ git clone https://github.com/GreenDragon/dotd_parser.git
```

Create the application settings file:
```
    $ cd <development_directory>/web2py/private
    $ cp apikey.example to apikey
```

Edit the apikey settings to reflect your environment
```
    apikey: <Super_Secret>
    platform: facebook
    game: dawn
    dbhost: localhost
    dbuser: root
    dbpass: password
    db: dotd_parser
    verbose_mode: 0
```
Replace the hash variables to the appropriate values you're using.
    game can be:        dawn or suns
    platform can be:    armor, facebook, kongegate, or newgrounds
    
    Platforms have been observed to be equal across games during testing
    
    verbose_mode makes item_import.py chatty

Create the application database:
```
    $ mysql
    mysql> CREATE DATABASE dotd_parser;
    mysql> GRANT ALL PRIVILEGES ON dotd_parser.* TO "dotd_parser"@"localhost" IDENTIFIED BY "password"; 
    mysql> FLUSH PRIVILEGES;
    mysql> EXIT
```

### Running the app:

Start up the web2py application:
```
    $ cd <development_directory>/web2py
    $ python web2py.py
```

Open the local instance to initialize the database:
```
    Open a browser to http://127.0.0.1:8000/
    Access admin menu
    Access dotd_parser app
    You should see a form entry
```

Populate the database with content from the UgUp API Server:
```
    $ cd <development_directory>/web2py/cron
    $ ./item_import.py
```

Go to your local instance and start testing:
```
    Open a browser to http://127.0.0.1:8000/
    Submit some raid logs
    You should see reports
```

### Production Installation:

Prep the *dotd_parser* for your production server:
```
    Open a browser to http://127.0.0.1:800/
    Switch to the admin mode
    Compile add working code
```

On your production server, configure a web2py instance:
```
    Create mysql database and user
    Extract web2py_src.zip to /content/${PROD.SERVER.TLD}/
    Adjust /content/${PROD.SERVER.TLD}/web2py/private/apikey for mysql credentials
    Copy <development_dir>/web2py/applications/dotd_parser/* to production server vhost dir
    Copy /content/${PROD.SERVER.TLD}/web2py/applications/dotd_parser/routes.production-mode.py 
        to /content/${PROD.SERVER.TLD}/web2py/routes.py
    Copy /content/${PROD.SERVER.TLD}/web2py/handlers/wsgihandler.py 
        to /content/${PROD.SERVER.TLD}/web2py/wsgihandler.py
    $ sudo chown -R www-data:www-data /content/${PROD.SERVER.TLD}/web2py/
```

Create a vhost instance in apache2:
```
    $ cd /etc/apache/sites-enabled
    $ sudo vi vhost-dotd-parser.conf
```

Apache VHost Entry:
    Replace ${IP_ADDRESS} with your servers IP Address
    Replace ${PROD.SERVER.TLD} with your vhost FQDN name

```
<VirtualHost ${IP_ADDRESS}:80>

ServerAdmin     webmaster@${PROD.SERVER.TLD}
ServerName      ${PROD.SERVER.TLD}

CustomLog       logs/${PROD.SERVER.TLD}-access_log combined
ErrorLog        logs/${PROD.SERVER.TLD}-error_log

WSGIDaemonProcess ${PROD.SERVER.TLD} user=www-data group=www-data processes=5 threads=1

WSGIProcessGroup ${PROD.SERVER.TLD}
WSGIScriptAlias / /content/${PROD.SERVER.TLD}/web2py/wsgihandler.py

# WSGIPassAuthorization On

<Directory /content/${PROD.SERVER.TLD}/web2py>
    AllowOverride None
    Order Allow,Deny
    Deny from all
    <Files wsgihandler.py>
      Allow from all
    </Files>
</Directory>

  AliasMatch ^/([^/]+)/static/(?:_[\d]+.[\d]+.[\d]+/)?(.*) \
        /content/${PROD.SERVER.TLD}/web2py/applications/$1/static/$2

  <Directory /content/${PROD.SERVER.TLD}/web2py/applications/*/static/>
    Options -Indexes
    ExpiresActive On
    ExpiresDefault "access plus 1 hour"
    Order allow,deny
    Allow from all
  </Directory>

</VirtualHost>
```

Check to see if apache is happy:
```
    $ sudo apache2ctl configtest
```

If so, restart apache:
```
    $ sudo /etc/init.d/apache2 restart
```

Access your VHost site via a browser.
```
    Go to http://${PROD.SERVER.TLD}/.
    You should see the dotd_parser app running with a prompt to enter log data
```

Populate the production server database with UgUp API content
```
    $ cd /content/${PROD.SERVER.TLD}/web2py/applications/dotd_parser/cron
    $ ./item_import.py
```

Go to your server instance and start testing:
```
    Open a browser to http://${PROD.SERVER.TLD}/
    Enter some log data and submit
    You should see a report
```

### Bugs/Issues/Requests...:

Please post an issue.

Better yet, fork and offer a pull request!

### Kudos:

Initial application conceived by https://github.com/tsunam/dotd_parser. 

Thanks!
