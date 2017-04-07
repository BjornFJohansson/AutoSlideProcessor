#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
Creates folders in the current working directory. The folders names should 
be present in the text file specified by <path> one name per line.

Usage: folder_generator <path>
       folder_generator -h|--help
       folder_generator -v|--version

Arguments:
    <path>  path to text file containing folder names, one per line

Options:
    -h, --help      Show this screen.
    -v, --version   Show version.
"""
__version__ = "1.0.0"
import os
import sys
import docopt
import codecs

#cwd = os.getcwd()
#script_dir = os.path.dirname(os.path.realpath(__file__))
#os.chdir(script_dir)
folders=[]
try:
    arguments = docopt.docopt(__doc__)
except docopt.DocoptExit as e:
    print(e.usage)
    sys.exit(1)

if arguments["--version"]:
    print(__version__)

if arguments["<path>"]:
    file_ = arguments["<path>"]
    try:
        with codecs.open(file_, "rU", 'utf8') as f: 
            folders=f.read().splitlines()
    except IOError:
        print(arguments["<path>"], "could not be opened!")
        sys.exit(1)

assert len(folders)==len(set(folders))

for folder in folders:
    try:
        os.mkdir(folder)
    except FileExistsError:
        print(folder, "already exists and was not created.")
#os.chdir(cwd)