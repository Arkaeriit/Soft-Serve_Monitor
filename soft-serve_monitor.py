#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
from flask import Flask, render_template
import markdown

# --------------------------------- Constants -------------------------------- #

ERR_OK             = 0
ERR_ARG            = 1
ERR_FILE_NOT_FOUND = 2
ERR_JSON           = 3
ERR_MISSING_KEY    = 3

CONFIG_KEYS = ["ss_host", "ss_port", "repos_path", "monitor_port", "monitor_name"]

HTLM_STYLE = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans&display=swap" rel="stylesheet"> 
<link rel="stylesheet" href='/static/style.css' />
"""

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

# -------------------------- Preparing server's state ------------------------ #

if __name__ == '__main__':
    app = Flask(__name__)

# -------------------- Listing repositories in the server -------------------- #

def list_repos_in_server():
    "Returns a list of all the repositories in the server."
    return os.listdir(config["repos_path"])

def clone_cmd(repo_name):
    "From the repository name returns the git command to clone it."
    prefix = "git clone ssh://"
    return prefix + config["ss_host"] + ":" + str(config["ss_port"]) + "/" + repo_name

def repos_description():
    """Generate an list presenting all repositories on the server and a dic
    of the command to clone them."""
    ret1 = list_repos_in_server()
    ret2 = {}
    for i in ret1:
        ret2[i] = clone_cmd(i)
    return ret1, ret2

# ------------------------ Managing list of README.md ------------------------ #

def get_file_in_repos(repo_name, filename):
    """This function tries to get a file from a repo in its main branch.
    It the file is found, True and its content are returned. If not,
    False and a random string are returned."""
    goto_repo = "cd "+config["repos_path"]+"/"+repo_name+" && "
    branch_cmd = os.popen(goto_repo + "git rev-parse --abbrev-ref HEAD 2> /dev/null")
    branch = branch_cmd.read().split("\n")[0]
    branch_cmd.close()
    os.system(goto_repo + "git symbolic-ref HEAD refs/heads/"+branch)
    show_cmd = os.popen(goto_repo + "git show "+branch+":"+filename+" 2> /dev/null")
    content = show_cmd.read()
    exit_code = show_cmd.close()
    return exit_code == None, content

def get_readme(repo_name):
    """Tries to get README.md or README.txt or README in a repo and if none
    is found, creates a placeholder one."""
    file_ok, readme = get_file_in_repos(repo_name, "README.md")
    if file_ok:
        return readme
    file_ok, readme = get_file_in_repos(repo_name, "README.txt")
    if file_ok:
        return readme
    file_ok, readme = get_file_in_repos(repo_name, "README")
    if file_ok:
        return readme
    readme = "# "+repo_name+"\n\n_No README for this repository._\n"
    return readme

@app.route("/<string:repo_name>")
@app.route("/<string:repo_name>/")
def present_repo(repo_name):
    "This function renders the webpage presenting a repository."
    repo_list, cmd_dic = repos_description()
    try:
        cmd = cmd_dic[repo_name]
        readme_md = get_readme(repo_name)
        readme = markdown.markdown(readme_md, extensions=['tables', 'extra'])
        return render_template("repo.html", repo_name = repo_name, cmd = cmd, readme = readme, server_name = config["monitor_name"], style = HTLM_STYLE)
    except KeyError:
        return render_template("repo_not_found.html", repo_name = repo_name, server_name = config["monitor_name"], style = HTLM_STYLE), 404


# --------------------------------- Web page --------------------------------- #

@app.route('/')
def webpage(rest=None):
    ssh_command = "ssh -p "+str(config["ss_port"])+ " "+config["ss_host"]
    push_target = "ssh://"+str(config["ss_host"])+":"+str(config["ss_port"])+"/<repository name>"
    repo_list, cmd_dic = repos_description()
    return render_template("index.html", server_name = config["monitor_name"], ssh_command = ssh_command, repo_list = repo_list, style = HTLM_STYLE, push_target = push_target)

@app.errorhandler(404)
def page_not_found(e):
    print(e)
    return render_template('404.html', style = HTLM_STYLE), 404

# ---------------------------- Running the server ---------------------------- #

if __name__ == '__main__':
    app.run(port = config["monitor_port"])

