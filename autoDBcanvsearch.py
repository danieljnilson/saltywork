# -*- coding: utf-8 -*-
# Using BioPython to download the Protein Coding Sequences from Archaea Genomes
# Performs genome annotations using dbCAN
# By Daniel Nilson, 9/11/2013

from Bio import Entrez
import os
import subprocess
import csv
Entrez.email = "danieljnilson@gmail.com"

## Directory Correction

home = os.getenv("HOME")

## Generating Dictionary/Array of Archaea Species and their Corresponding Accession Numbers

myfilepath = home + "/saltywork/Accessions.csv" #Erin's file
Col1 = "Organism"
Col2 = "Accession#"
Col3 = "BioPROJECT"
mydictionary={Col1:[], Col2:[], Col3:[] } #Making an array in python
csvFile = csv.reader(open(myfilepath, "rU")) # the "rU" is there to alleviate an issue with headerless CSVs
firstline = True
for row in csvFile:
    if firstline:    #skip first line
        firstline = False
        continue
    mydictionary[Col1].append(row[0])
    mydictionary[Col2].append(row[1])
    mydictionary[Col3].append(row[2])

# Generate aaFASTA file name for organism, then precede to download aaFASTA sequence, scan it, and parse it.
# Then moves on to the next organism.
loops = len(mydictionary['Organism'])

for i in range(67):
    
    filename = home + "/saltywork/data/seq/" + mydictionary['Organism'][i] + ".faa" #Dumps FASTA file here
    filename = filename.replace(" ","")    
    if not os.path.isfile(filename): #checks if amino acid sequence of genome is present already
        if not os.path.exists(os.path.dirname(filename)): # Checks to see if directory is already there
            os.makedirs(os.path.dirname(filename)) # Makes directory     
    
        # Finds all proteins associated with BioPROJECT ID, two step process
        searchResultHandle = Entrez.esearch(db="protein", term=mydictionary['BioPROJECT'][i], usehistory="y")
        searchResult = Entrez.read(searchResultHandle)
        searchResultHandle.close()
        print "Identifier list made for " + mydictionary['Organism'][i]
        gi_list = searchResult["IdList"]
       # uidList = ','.join(searchResult['IdList']) # Makes list from search result
        print gi_list
        webenvV = searchResult["WebEnv"]
        query_keyV = searchResult["QueryKey"]
        count = int(searchResult["Count"])
        batch_size = 100
        
        out_handle = open(filename, 'w') # My file is opened
        for j in range(0,count,batch_size):
            end = min(count, j + batch_size)
            print "Downloading record of %i to %i" % (j + 1, end)
            net_handle = Entrez.efetch(db="protein", rettype='fasta',retstart=j, retmax=batch_size, webenv = webenvV, query_key = query_keyV)# Information from NCBI is read into here
            data = net_handle.read() # From from NCBI is written through reading into my file
            net_handle.close()
            out_handle.write(data)
        out_handle.close() # closing file writing pipeline
        
        print "Saved " + mydictionary['Organism'][i]
    
    os.chdir(home+"/dbCAN") # Changes the BASH directory to HMMER's location. Ensures that HMMER works.
    ### HMMER Scan ###
    HMMfile= home + "/saltywork/data/results/HMM/"+'HMM'+mydictionary['Organism'][i]+'.out'
    HMMfile = HMMfile.replace(" ","")
    if not os.path.isfile(HMMfile): # checks if homologs have already been determined
        print "Finding protein sequences homologs of " + mydictionary['Organism'][i]
        if not os.path.exists(os.path.dirname(HMMfile)): # Checks to see if directory is already there
                os.makedirs(os.path.dirname(HMMfile)) # Makes directory 
        with open(HMMfile,'w') as out:
            output = subprocess.call(["hmmscan","dbCAN-fam-HMMs.txt",filename],stdout=out)
        out.closed
        print "HMMed " + mydictionary['Organism'][i]
        ### Parsing Step ###
       
    Parsefile = home + "/saltywork/data/results/HMM/"+'P'+mydictionary['Organism'][i]+'.ps'
    if not os.path.isfile(Parsefile): # checks if homologs have already parsed
        with open(Parsefile,'w') as out:
            output = subprocess.call(["sh","hmmscan-parser.sh",HMMfile],stdout=out)
        out.closed
        print "Parsed " + mydictionary['Organism'][i]