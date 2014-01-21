# -*- coding: utf-8 -*-
# Using BioPython to download the Protein Coding Sequences from Archaea Genomes
# By Daniel Nilson, 9/11/2013

from Bio import Entrez
import os
import subprocess
import csv
Entrez.email = "danieljnilson@gmail.com"

## Generating Dictionary/Array of Archaea Species and their Corresponding Accession Numbers

myfilepath = "/home/daniel/dbCAN/Accessions.csv" #Erin's file
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
    mydictionary[Col1].append(row[0])response = urllib2.urlopen(url)
    mydictionary[Col2].append(row[1])
    mydictionary[Col3].append(row[2])

# Generate aaFASTA file name for organism, then precede to download aaFASTA sequence, scan it, and parse it.
# Then moves on to the next organism.
loops = len(mydictionary['Organism'])

for i in range(1):
    
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
    
    filename = mydictionary['Organism'][i] + ".faa" #Dumps FASTA file here
    filename = filename.replace(" ","")

    batch_size = 100
    
    if not os.path.isfile(filename):    
        # Downloading...can't see .folder in ubuntu
        #net_handle = Entrez.efetch(db="nuccore", id="NC_013158", rettype="fasta_cds_aa")
        #rec = Entrez.read(Entrez.esearch(db="protein", term=mydictionary['Accession#'][i])
        out_handle = open(filename, "w") # My file is opened
        for j in range(0,count,batch_size):
            end = min(count, j + batch_size)
            print "Going to download record %i to %i" % (j + 1, end)
            net_handle = Entrez.efetch(db="protein", rettype='fasta',retstart=j, retmax=batch_size, webenv = webenvV, query_key = query_keyV)# Information from NCBI is read into here
            data = net_handle.read() # From from NCBI is written through reading into my file
            net_handle.close()
            out_handle.write(data)
        out_handle.close() # closing file writing pipeline
        
        print "Saved " + mydictionary['Organism'][i]
    
    os.chdir("/home/daniel/dbCAN") # Ensures that HMMER works.
    ### HMMER Scan ###
    HMMfile='HMM'+mydictionary['Organism'][i]+'.out'
    HMMfile = HMMfile.replace(" ","")
    with open(HMMfile,'w') as out:
        output = subprocess.call(["hmmscan","dbCAN-fam-HMMs.txt",filename],stdout=out)
    out.closed
    print "HMMed " + mydictionary['Organism'][i]
    ### Parsing Step ###
    Parsefile = 'P'+mydictionary['Organism'][i]+'.ps'
    with open(Parsefile,'w') as out:
        output = subprocess.call(["sh","hmmscan-parser.sh",HMMfile],stdout=out)
    out.closed
    print "Parsed " + mydictionary['Organism'][i]