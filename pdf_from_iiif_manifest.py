#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 08:59:01 2022

@author: jdummer
"""

'''This script uses the iiif manifests for items in Colenda to 
download jpegs for those items and create pdfs from the jpegs.'''

# import packages and modules needed to run the script

import json
import csv
from csv import writer
from csv import reader
import requests
import os
import re
import img2pdf
import sys


# create variables to use to build each iiif manifest url
iiif_manifest_prefix = "https://colenda.library.upenn.edu/phalt/iiif/2/81431-"
iiif_manifest_suffix = "/manifest"
path = os.getcwd()


'''Build a function to eliminate whitespace'''

RE_WHITESPACE = re.compile(r"\s+")
def normalize_string(s):
    return RE_WHITESPACE.sub(' ', s).strip()

'''Build a function that takes input from a text file that contains an id
on each line and returns a list of those ids.'''

def arkids(data) -> list:
    id_list = []
    for line in data:
        id_list.append(normalize_string(line))
    return id_list

'''Build a function that takes an the unique part of the ark id as a
parameter and concatenates a prefix and suffix to the id to create a Colenda
iiif manifest for that id.'''

def iiif_manifest_url(ark) -> str:
    iiif_manifest = iiif_manifest_prefix + ark + iiif_manifest_suffix
    return normalize_string(iiif_manifest)

'''Build a function that forms a variable that is the image path in the iiif
manifest json, then request to get that image, and write it to the directory
with the arkid for that item. Use the number parameter to provide the sequence
number of that jpeg in the manifest.''' 

def get_jpeg(number, dictionary):
    image = dictionary["images"][0]["resource"]["service"]["@id"] + "/full/,1800/0/default.jpg"
    r = requests.get(image)
    with open(f'{folder_name}/{folder_name}_{"%03d" % number}.tif', 'wb') as f:
        f.write(r.content)
        f.close()

'''Build a function that takes a list of files as the parameter, sorts them
in numerical order and builds a pdf of those files.'''
        
def build_pdf(files):
    files.sort()
    f.write(img2pdf.convert(files))
    f.close()

    
# The text file entered by the user is saved to the variable input_file
input_file = sys.argv[1]

with open(input_file, 'r') as data:
    ark_id_list = arkids(data)  # rename the id_list returned by arkids() 

# print a message that the ark_id_list has been created
print('Ark ID list created\n')

# print a message that the iiif_manifest_list was created
print('The iiif manifest list was created\n')


''''For each ark id in the ark_id_list, create a directory named with the
arkid string, then get the iiif_manifest_url for that id. Use the url to
get the iiif manifest as json and use the json to get all the full-size
jpegs and download them to the arkid folder.'''
     
for arkid in ark_id_list: 
    
    if os.path.exists(arkid):
        print(f'Error: folder exists: {arkid}.')
        sys.exit(1)
    os.mkdir(arkid)
    folder_name = arkid
    x = iiif_manifest_url(arkid)
    r = requests.get(x) # Use requests to get the iiif manifest as json
    data = r.json()
    canvases = data["sequences"][0]["canvases"]
    # Print a message when the process of dowloading jpegs is ready to begin.    
    print('Accessing images for ark id: ' + arkid + '\n')

    # Loop over the canvases in the iiif manifest and call the get_jpeg()
    # function to get each full-size jpeg in the manifest and downloading
    # them in order starting with 0 to the folder with the arkid for that item.

    i = 0
    for canvas in canvases:
        get_jpeg(i, canvas)
        i += 1

    # Print a message when all the images are dowloaded for an item.
    print('Dowloaded images for ark id: ' + arkid + '\n')

    # create a list of files from the files in a directory with an ark id and 
    # call the build_pdf() fucntion on those files to create a pdf for the
    # ark        
    
    with open(f'{path}/{arkid}/{arkid}.pdf', 'wb') as f:
        files = [f'{arkid}/{i}' for i in os.listdir(arkid) if i.endswith('.tif')]
        build_pdf(files)
    print('PDF created for ark id: ' + arkid + '\n')
    
print('Done!')    




