#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pathlib      
# only in python 3, see https://pypi.python.org/pypi/pathlib2/2.1.0 for python 2.7
##########################################################
FOLDERLOCATION = pathlib.Path("/Public/BLACKBOARD")
FOLDERNAME     = pathlib.Path("MyAwesomeCourse")
TOKENNAME      = "DROPBOXTOKEN"
##########################################################

import re
import os
import sys

import subprocess
import codecs
import dropbox      # https://pypi.python.org/pypi/dropbox

print("dropbox.__version__ =", dropbox.__version__)
import requests
print("requests.__version__=", requests.__version__)
del requests

########################################################
#with open(".cached_sha1_checksum/last.sha1", "w") as f:
#    f.write('f14ba6fab9f5e3ff72ce21f90a10f2de4d7d186f')
########################################################

def newsuffix(p):
    try:
        return {".odt": ".pdf",
                ".odp": ".pdf",
                ".ods": ".xlsx",
                ".md" : ".pdf"}[p.suffix.lower()]
    except KeyError:
        return p.suffix.lower()
        
#============================== Connect to Dropbox ===========================
with open(".continuous_integration/dropbox_token.txt", "r") as f:
    TOKEN = f.read().strip()
if not TOKEN:
    TOKEN = os.getenv(TOKENNAME, "NONE")
dbx = dropbox.Dropbox(TOKEN)
try:
    dbx.users_get_current_account()
except dropbox.exceptions.AuthError as err:
    sys.exit("ERROR: Invalid access token; try re-generating an access token"
             "from the app console on the web.")

    
#===============check if remote folder is empty ==============================        


if dbx.files_list_folder(str(FOLDERLOCATION.joinpath(FOLDERNAME))).entries:
    remote_empty = False
else:
    remote_empty = True

print("try to open cached_sha1_checksum/last.sha1")

try:
    f = open(".cached_sha1_checksum/last.sha1", "r")
except FileNotFoundError:
    print("\nNO file called .cached_sha1_checksum/last.sha1 found!\n")
    oldsum = ""
else:
    oldsum = f.read().strip()
    print(".cached_sha1_checksum/last.sha1 read from file:")
    print(oldsum)
    print()
    f.close()

cmd="git rev-list HEAD".split()
result = subprocess.run(cmd, stdout=subprocess.PIPE)
commits = result.stdout.decode().split()[::-1]
newsum = commits[-1]

if oldsum and not remote_empty:  
    
    commits = commits[commits.index(oldsum):]

    oldsum = commits[0]
    
    print("files changed between commits", oldsum, newsum)
    cmd = "git diff --name-status --diff-filter=R".split()
    result = subprocess.run( cmd+[oldsum, newsum], stdout=subprocess.PIPE, universal_newlines=True)
    output = codecs.escape_decode(result.stdout, "utf-8")[0].decode("utf-8")
    lines_ = output.strip().splitlines()
    old_files =[pathlib.Path(old.strip('"')) for letter,old,new in [l.split("\t") for l in lines_]]

    cmd = "git diff --name-only --diff-filter=D".split()
    result = subprocess.run( cmd+[oldsum, newsum], stdout=subprocess.PIPE, universal_newlines=True)
    output = codecs.escape_decode(result.stdout, "utf-8")[0].decode("utf-8")
    deleted_files = [pathlib.Path(f) for f in output.strip().splitlines()]
    deleted_files = deleted_files + old_files
    
    cmd = "git diff --name-only --diff-filter=rd".split()
    result = subprocess.run( cmd+[oldsum, newsum], stdout=subprocess.PIPE, universal_newlines=True)    
    output = codecs.escape_decode(result.stdout, "utf-8")[0].decode("utf-8")
    added_files = [pathlib.Path(f) for f in output.strip().splitlines()]
    
else:
    print("All files will be processed")
    print("remote empty", remote_empty)
    deleted_files = []
    added_files = [pathlib.Path(root).joinpath(name)
                 for root, dirs, files in os.walk(".")
                 for name in files]
    renamed_files = []

added_files = [p for p in added_files if not [d for d in p.parts if d.startswith(("_","."))]]

os.makedirs(".cached_sha1_checksum", exist_ok=True)
with open(".cached_sha1_checksum/last.sha1", "w") as f:
    f.write(newsum)

print("The following paths will be deleted remotely:")

if deleted_files:
    for pth in deleted_files:
        npth = pth.with_suffix(newsuffix(pth))
        print(npth)
        try:
            dbx.files_delete(str(FOLDERLOCATION.joinpath(FOLDERNAME, npth)))
        except dropbox.exceptions.ApiError as err:
            if (err.error.get_path_lookup() and err.error.get_path_lookup().is_not_found()):
                print(npth, " not found.")
            elif err.user_message_text:
                print(err.user_message_text)
                #sys.exit()
            else:
                print(err)
                #sys.exit()  
else:
    print("NO files deleted remotely.\n")

print("The following new paths will be added to remote:")
if added_files:
    for pth in added_files:
        if pth.suffix.lower() in (".odt", ".odp", ".odg"): # writer, impress --> pdf
            cmd = "libreoffice --invisible --convert-to pdf".split()
            cmd.extend((str(pth), "--outdir", str(pth.parent)))
            print(" ".join(cmd)) 
            result = subprocess.run( cmd, stdout=subprocess.PIPE)
            print(" ".join(result.args))
            print(result.stdout)
            print()
            npth = pth.with_suffix(".pdf")
        elif pth.suffix.lower() == ".ods":  # calc --> Excel
            cmd = "libreoffice --invisible --convert-to xlsx".split()
            cmd.extend((str(pth), "--outdir", str(pth.parent)))
            print(" ".join(cmd))
            result = subprocess.run( cmd, stdout=subprocess.PIPE)
            print(" ".join(result.args))
            print(result.stdout)      
            print()
            npth = pth.with_suffix(".xlsx")
        elif pth.suffix.lower() == ".md":  # markdown --> pdf
            cwd = os.getcwd()
            os.chdir(str(pth.parent))       
            if str(pth) == "README.md":
                cmd = "pandoc README.md -o README.html --self-contained".split() # --css .continuous_integration/pandoc.css
                sfx=".html"
            else:
                cmd = 'pandoc --latex-engine=xelatex'.split()
                cmd.append(pth.name)
                cmd.append("-o")
                cmd.append(pth.with_suffix(".pdf").name)
                sfx=".pdf"
            print(" ".join(cmd)) 
            result = subprocess.run( cmd, stdout=subprocess.PIPE)
            print(" ".join(result.args))
            print(result.stdout)
            print()
            os.chdir(cwd)
            npth = pth.with_suffix(sfx)
        elif pth.suffix.lower() in (".txt", ".fa", ".gb", ".fasta"):
            with open(str(pth)) as f:
                new = re.sub("\r?\n", "\r\n", f.read())
            with open(str(pth), "w") as f:
                f.write(new)
            npth = pth
        else:
            npth = pth
            
        rempth = FOLDERLOCATION.joinpath(FOLDERNAME, npth)
        print("uploading", npth, "to", rempth)
        print()
        with npth.open('rb') as f:
            try:
                dbx.files_upload(f, 
                                 str(rempth), 
                                 mode=dropbox.files.WriteMode('overwrite'))
            except dropbox.exceptions.ApiError as err:
                if (err.error.is_path() and
                        err.error.get_path().error.is_insufficient_space()):
                    sys.exit("ERROR: Cannot back up; insufficient space.")
                elif err.user_message_text:
                    print(err.user_message_text)
                    #sys.exit()
                else:
                    print(err)
                    #sys.exit()        
else:
    print("NO new paths added to remote\n")

print("done!")

