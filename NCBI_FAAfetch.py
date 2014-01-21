# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 11:35:46 2013

@author: daniel
"""

# By Daniel Nilson
#
# Downloads sequences



from Bio import Entrez
import os
import csv
Entrez.email = "danieljnilson@gmail.com"

## Generating Dictionary/Array of Archaea Species and their Corresponding Accession Numbers

dbCAN = "/home/daniel/dbCAN/" # File path to dBCAN and everything else.
myfilepath = dbCAN + "cazyGH109-S9-genes.csv" #Erin's file
Faapath = dbCAN + "Data/"
SaveData = dbCAN + "Data/" + "cazyGH109-S1" + "/" # To prevent clutter inside the dbCAN folder
Genelist = dbCAN + "cazyGH109-S1-genes.csv"

if not os.path.exists(SaveData):
    os.makedirs(SaveData)

# Constructing a dictionary from Erin's Accessions.csv

Col1 = "Organism"
Col2 = "GeneID"
mydictionary={Col1:[],Col2:[] } #Making an array in python
csvFile = csv.reader(open(Genelist, "rU")) # the "rU" is there to alleviate an issue with headerless CSVs
firstline = True
for row in csvFile:
    if firstline:    #skip first line
        firstline = False
        continue
    mydictionary[Col1].append(row[0])
    mydictionary[Col2].append(row[1])

# Generate aaFASTA file name for organism, then precede to download aaFASTA sequence

loops = len(mydictionary['GeneID'])
filename = SaveData + "cazyGH109-S1-genes.faa"

for i in range(loops):
    # Downloading...can't see .folder in ubuntu
    #net_handle = Entrez.efetch(db="nuccore", id="NC_013158", rettype="fasta_cds_aa")
    #rec = Entrez.read(Entrez.esearch(db="protein", term=mydictionary['Accession#'][i])
    net_handle = Entrez.efetch(db="nuccore", id = mydictionary['GeneID'][i], rettype="fasta_cds_aa")# Information from NCBI is read into here
    out_handle = open(filename, "a+") # My file is opened and appended
    out_handle.write(net_handle.read()) # From from NCBI is written through reading into my file
    out_handle.close() # closing pipelines
    net_handle.close()
    print "Saved " + mydictionary['GeneID'][i]
    
    

