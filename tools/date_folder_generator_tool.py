#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script will look for folders in the cwd 
that has a name that is a valid isodate: yyyy-mm-dd. 

If found, the latest folder will be chosen. 
51 new folders will be generated with names that 
are one week apart.
'''

import os
import datetime
import time

folders = [ f for f in os.listdir(".") if os.path.isdir(f) ]
datefolders = []

for f in folders:
    try:
        date = datetime.date(*time.strptime(f, "%Y-%m-%d")[0:3])
    except ValueError:
        continue
    datefolders.append(date)

folder = max(datefolders)

dates = ("{} {}".format(d.isoformat(), d.strftime("%A")) for d in [folder + datetime.timedelta(weeks=n) for n in range(1,52)])

for d in dates:
    os.mkdir(d)
    
print("date_folder_list_generator is done!")
