#!/bin/bash

BASE="http://ugup.5thplanetgames.com/api/"
SLEEP=5
SECRETS_FILE=~/.ugup.secrets
DATA="data"

exit_with_error () {
  echo
  echo "Exiting..."
  exit 1
}

CURL=`which curl`
if [ -z "${CURL}" ]; then
  echo
  echo "Expected to have the curl utility installed."
  echo "Please install from http://curl.haxx.se/."
  exit_with_error
fi

if [ ! -f ${SECRETS_FILE} ]; then
  echo
  echo "Expected to file a UgUp secrets file @ ${SECRETS_FILE}"
  exit_with_error
else
  source ${SECRETS_FILE}
fi

if [ -z "${API_KEY}" ]; then
  echo
  echo "Expected API_KEY definition."
  echo
  echo "Did you create a ${SECRETS_FILE} file with your UgUp API key?"
  echo
  echo "This file should have one line, with the format:"
  echo
  echo "API_KEY=_Your_UgUp_API_Key_"
  exit_with_error
fi

get_url () {
  if [ -z "${3}" ]; then
    echo "Missing required parameters!"
    return
  fi
  # ITEM=$1, PLATFORM=$2, GAME=$3
  URL="${BASE}${1}/definition/all?apikey=${API_KEY}&platform=${2}&game=${3}"
  echo "Working on URL: ${URL}"
  curl -o ${DATA}/${2}/${3}/${1}.${2}.${3}.json "${URL}"
  echo "Sleeping for ${SLEEP} seconds..."
  sleep ${SLEEP}
}

for platform in facebook kongregate armor newgrounds; do
  for game in dawn suns; do
    if [ ! -d ${DATA}/${platform}/${game} ]; then
      mkdir -p ${DATA}/${platform}/${game}
    fi
    get_url "equipment"   "${platform}" "${game}"
    get_url "mount"       "${platform}" "${game}"
    get_url "collection"  "${platform}" "${game}"
    get_url "general"     "${platform}" "${game}"
    get_url "troop"       "${platform}" "${game}"
    get_url "legion"      "${platform}" "${game}"
    get_url "consumable"  "${platform}" "${game}"
    get_url "magic"       "${platform}" "${game}"
    get_url "tactic"      "${platform}" "${game}"
    get_url "enchant"     "${platform}" "${game}"
    get_url "itemset"     "${platform}" "${game}"
    get_url "pet"         "${platform}" "${game}"
    get_url "recipe"      "${platform}" "${game}"
    get_url "achievement" "${platform}" "${game}"
    get_url "engineering" "${platform}" "${game}"
    get_url "raid"        "${platform}" "${game}"
  done
done
