#!/bin/bash

cd /${WEB2PY_HOME}/web2py/applications/dotd_parser/cron

for platform in facebook kongregate armor newgrounds; do
  for table in armor fb kong ng; do
    for server in 1 2; do
      # echo "Updating DotD ${plaform} ${table} ${server}..."
      ./get_shared_raid_details.py dawn_shared_raids_${table}_s${server} dawn ${platform} ${server}
    done
  done
done
