#!/bin/bash

cd /${WEB2PY_HOME}/applications/dotd_parser/cron

#echo "Updating LoTS Facebook"
./get_shared_raid_details.py suns_shared_raids       suns facebook 1

#echo "Updating LoTS Armor Games"
./get_shared_raid_details.py suns_shared_raids_armor suns armor 1

#echo "Updating LoTS Kongregate"
./get_shared_raid_details.py suns_shared_raids_kong  suns kongregate 1

#echo "Updating LoTS Newgrounds"
./get_shared_raid_details.py suns_shared_raids_ng    suns newgrounds 1
