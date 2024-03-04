#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 12:50:01 2023

@author: jdummer
"""

import requests
import sys
import time


while True:
    try:
        lists = open("iiifmanifests.txt")
        for line in lists:
            line = line.strip()
            time.sleep(2)
            r = requests.get(line)
            if r.status_code != 200:
                print(line)
                print(r.status_code)
    except requests.exceptions.ConnectionError as e:
        sys.exit(str(e))