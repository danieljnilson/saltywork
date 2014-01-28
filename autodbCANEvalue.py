# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 14:14:02 2013

@author: daniel
"""

# By Daniel Nilson
#
# Re-HMMERs Archaea genomes against CAZY database with a max E value
# Creates new excelfile



import os
import subprocess
import csv
import xlsxwriter

Evalue = "1e-20"
Ename = "EVAL1e-20"

## Directory Correction

home = os.getenv("HOME")


## Generating Dictionary/Array of Archaea Species and their Corresponding Accession Numbers

dbCAN = home + "/dbCAN/" # File path to dBCAN and everything else.
myfilepath = home + "/saltywork/"
Accessionpath = myfilepath + "Accessions.csv" #Erin's UC Davis Haloarchaea Accessions file
Faapath = myfilepath + "data/seq/"
SaveData = myfilepath + "data/results/HMM/" + Ename + "/" # To prevent clutter inside the folder

if not os.path.exists(SaveData):
    os.makedirs(SaveData)

# Constructing a dictionary from Erin's Accessions.csv

Col1 = "Organism"
Col2 = "Accession#"
Col3 = "BioPROJECT"
mydictionary={Col1:[], Col2:[], Col3:[] } #Making an array in python
csvFile = csv.reader(open(Accessionpath, "rU")) # the "rU" is there to alleviate an issue with headerless CSVs
firstline = True
for row in csvFile:
    if firstline:    #skip first line
        firstline = False
        continue
    mydictionary[Col1].append(row[0])
    mydictionary[Col2].append(row[1])
    mydictionary[Col3].append(row[2])

loops = len(mydictionary['Organism'])

for i in range(loops):
    filename = mydictionary['Organism'][i] + ".faa" #FASTA file here
    filename = filename.replace(" ","")

    
    os.chdir(dbCAN) # Ensures that HMMER works.
#    ## HAMMER TIME ###
    HMMfile='HMM'+mydictionary['Organism'][i]+Ename+'.out'
    HMMfile = HMMfile.replace(" ","")
    print "It's Hammer Time for " + mydictionary['Organism'][i]
    with open(SaveData+HMMfile,'w') as out:
        output = subprocess.call(["hmmscan","-E",Evalue,"dbCAN-fam-HMMs.txt",Faapath+filename],stdout=out) # Performs HMM, saves to directory underlined in SaveData+filename
    out.closed
    print "HMMed " + mydictionary['Organism'][i]
    ### CAN'T PARSE THIS ###
    print "Parsing " + mydictionary['Organism'][i]
    Parsefile = 'P'+mydictionary['Organism'][i]+Ename+'.ps'
    Parsefile = Parsefile.replace(" ","")
    with open(SaveData+Parsefile,'w') as out:
        output = subprocess.call(["sh","hmmscan-parser.sh",SaveData+HMMfile],stdout=out)
    out.closed
    print "Parsed " + mydictionary['Organism'][i]
    
## Make Excel File
## Compiles annotation data

workbook = xlsxwriter.Workbook(SaveData+Ename+'CompleteCAZYparse.xlsx')
worksheet = workbook.add_worksheet("GH Families")
worksheet.write(0,0,"Organism")

# Searches for proteins from GH families

for i in range(loops): ## Rows
    name = mydictionary['Organism'][i]
    name = name.replace(" ","")
    worksheet.write(i+1,0,mydictionary['Organism'][i]) # Writes Organism name in first column
    Parsefile = 'P'+name+Ename+'.ps' # File of dbCAN parsed results
    for j in range(132):                # 132 GH families, Columns
        n = str(j + 1)
        worksheet.write(0,j+1,"GH"+n)
        parse = "GH"+n+".hmm"
        n = int(n)
        input = str(open(SaveData+Parsefile).read())
        occurrence = input.count(parse)
        #output = subprocess.call(["grep","-c",parse,SaveData+Parsefile])
        worksheet.write(i+1,n,occurrence) # Writes Number of Hits
# Searches for proteins from AA families
worksheet2 = workbook.add_worksheet("AH Families")
worksheet2.write(0,0,"Organism")

for i in range(loops):
    name = mydictionary['Organism'][i]
    name = name.replace(" ","")
    worksheet2.write(i+1,0,mydictionary['Organism'][i]) # Writes Organism name in first column
    Parsefile = 'P'+name+Ename+'.ps' # File of dbCAN parsed results
    for j in range(10):                # 10 AA families
        n = str(j + 1)
        worksheet2.write(0,j+1,"AA"+n)
        parse = "AA"+n+".hmm"
        n = int(n)
        input = str(open(SaveData+Parsefile).read())
        occurrence = input.count(parse)
        #output = subprocess.call(["grep","-c",parse,SaveData+Parsefile])
        worksheet2.write(i+1,n,occurrence) # Writes Number of Hits
    
workbook.close()

