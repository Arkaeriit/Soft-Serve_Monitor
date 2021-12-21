#!/usr/bin/env python3

import os
import sys
import json

# --------------------------------- Constants -------------------------------- #

ERR_OK             = 0
ERR_ARG            = 1
ERR_FILE_NOT_FOUND = 2
ERR_JSON           = 3
ERR_MISSING_KEY    = 3

CONFIG_KEYS = ["ss_host", "ss_port", "repos_path", "monitor_port"]

# ------------------------ Opening configuration file ------------------------ #

def open_config():
    """This function opens the configuration file given as argument and checks
    that it's content is valid. If it is not valid, an error code is returned.
    If it is valid, ERR_OK and a dictionary with the configuration is returned.
    """
    # Checking argument
    try:
        config_file = sys.argv[1]
    except IndexError:
        sys.stderr.write("Error, no configuration file given as argument.\n")
        return ERR_ARG, None
    # Checking that the file contains valid JSON
    try:
        with open(config_file, "r") as f:
            config_dic = json.load(f)
    except json.decoder.JSONDecodeError:
        sys.stderr.write("Error while decoding JSON file. Verify that the syntax is correct.\n")
        return ERR_JSON, None
    except:
        sys.stderr.write("Error, unable to open configuration file.\n")
        return ERR_FILE_NOT_FOUND, None
    # Checking that all the needed fields are here
    try:
        for k in CONFIG_KEYS:
            config_dic[k]
    except KeyError:
        sys.stderr.write("Error, the configuration file does not contains all required fields.\n")
        sys.stderr.write("The required fields are:\n")
        for k in CONFIG_KEYS:
            sys.stderr.write("  - " + k + "\n")
        return ERR_MISSING_KEY, None
    return ERR_OK, config_dic

if __name__ == "__main__":
    config_err, config = open_config()
    if config_err != ERR_OK:
        sys.exit(config_err)

