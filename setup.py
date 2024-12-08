#!/usr/bin/env python

import os
config_file = "config.py"

if os.path.exists(config_file):
    print("Error: config.py already exists. Delete config.py to proceed.")
else:
    bot_api_key = input("Enter bot api key")

    f = open(config_file,"w")
    f.write("TOKEN = ")
    f.write(bot_api_key)
    f.write("\n")
    f.close()

    print("Wrote config")