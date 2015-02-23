2015.02.22  GreenDragon

Some command line utilities to gather the base json files from the API server for caching and processing purposes.

Store your UgUp API key in a secret file in your home directory

~/.ugup.secrets

With the format:

API_KEY="_Your_UgUp_API_Key_Value"
...

~~~

**get_base_data_sets/get-base-data-sets.sh**

This script assumes you have bash and curl installed.

This script walks through all the various *all* API calls from UgUp for 
each platform and game and stores them under ./$platform/$game with the
following format: ./$platform/$game/$name.$platform.$game.json.

- Questions: 
  - Is there any difference in data between the platforms?
    - A cursory examination seems to be *no*.
    - Tactic API call under LoTS (sun) is broken.
  - Is there going to be API calls for the Mobile platform?
    - Don't know...

**get_base_data_sets/dotd_parser.sql**

This is an initial pass at a new schema for the parser. Many of the rows are currently not used, but why postpone for a later date?


