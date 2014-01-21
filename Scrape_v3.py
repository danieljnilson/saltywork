# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:42:08 2013

@author: daniel
"""

from bs4 import BeautifulSoup
import urllib2
import os
import xlsxwriter
import time

# (1) This code will download all the Archaea annotation webpages from CAZY
#   a. Go through entire alphabet of Archaea
#   b. Find urls to each archaeaon of that alphabet
#   c. Download webpages
# (2) Parse them with Beautiful Soup
# (3) Collect data
# (4) Output data to an EXCEL sheet


## Global Variables
baseurl='http://www.cazy.org/a'

directory = '/home/daniel/UbuntuOne/PythonProjects/CAZYScrape/'



## Functions

def Readurl(url):
    response = urllib2.urlopen(url) # Object in which HTML page is initially read into
    htmlpage = response.read()
    return htmlpage    
    


workbook = xlsxwriter.Workbook('/home/daniel/UbuntuOne/PythonProjects/CAZYScrape/CAZyArchaea.xlsx')  # Makes Excel worksheet
worksheet = workbook.add_worksheet()
worksheet.write(0,0,'Organism')
col = 0
orgnum = 1

time.sleep(5) ## NECESSARY. Otherwise EXCEL sheet won't be made "in time"

for i in range(133): ## Makes labels for all GH families
    col = 1 + col
    GHstring = "GH"+str(i+1)
    worksheet.write(0,col,GHstring)
    if i == 133:
        worksheet.write(0,col,"NC")



for let in list(map(chr, range(ord('A'), ord('Z')+1))): ## Going through the alphabet.. A - Z
    url = baseurl + let + '.html'
    htmlpage = Readurl(url)
   
    soup = BeautifulSoup(htmlpage) # Makes soup object
    pagetitle = soup.title.get_text() # Grabs title of page, makes it the file nane
    pagetitle = pagetitle.replace(' ','')
    urlfile = directory + pagetitle + '_' + let + '.html' # Paorgnum = 1 # Keeps track of number of archaea that have been tabulated, is essentially the "row" in the EXCEL sheetge name with directory letter
    print('Checking to see if ' + urlfile + ' already exists!')
    if os.path.exists(urlfile): # Checks to see if html file exists of page yet, if not, downloads it
        pass
        print(urlfile + ' already exists, moving on to the next Archaea List page')
    else:
        print(urlfile + ' did not exist, downloading and analyzing.')
        ArchList = soup.find_all(class_="nav")# List of Archaea, for urls
        Llength = len(ArchList)
        if Llength > 0: # Checks to see if there are any archaea associated with that Letter, if not, program moves on to next letter
            with open(urlfile,'w') as out:
                out.write(htmlpage)
        print('Beginning Specific Archaeaon annotation page download beginning with letter ' + let) # Downloads list of all Archaea associated with letter

        for i in range(len(ArchList)):
            ArchList[i].string = ArchList[i].string.replace(' ','_') # Replaces spaces with "_"
            if ArchList[i].string.find('/') > 0: #Checks for invalid names
                ArchList[i].string = ArchList[i].string.replace('/','*') # Replaces "/" with *
            urlpage = ArchList[i].get('href')
            htmlpageAP = Readurl(urlpage) # Specific Archaea page is read
            directorylet = directory + let + '/'
            filename = directorylet + ArchList[i].string + '.html' # directory and filename of Archaea html file
            print('Checking to see if ' + filename + ' already exists!')
            if os.path.exists(filename): # Checks to see if html file exists of page yet, if not, downloads it
                pass
                print('It exists, moving on')
            else:
                if not os.path.exists(directorylet):
                    os.makedirs(directorylet)
                print('It did not exist, downloading page')
                with open(filename,'w') as out:
                    out.write(htmlpageAP)
                    print 'Writing html page of '+ ArchList[i].string

            ### Need to Scan the Page for GH hits now!
            Asoup = BeautifulSoup(open(filename))
            print("Analyzing HTML page of " + ArchList[i].string + "!")
            GHsoup = Asoup.find("th")
            row = orgnum
            print("Currently on organism number: " + str(orgnum))
            GHsoupinfo = list(GHsoup.find_next_siblings()) #Makes a list of all the GH family information that pops up in the HTML file
            famlen = len(list(GHsoup.find_next_siblings())) # Number of represented families
            col = 0
            worksheet.write(row, col, ArchList[i].string) # Writes down the archaea's name

            for j in range(famlen):
                GHfam = str(GHsoupinfo[j].find(class_='famille').string) # Outputs the GHfamily number
                if GHfam == 'NC':
                    GHfam = '133'
                col = int(GHfam)
                GHnum = str(GHsoupinfo[j].find(class_='nombre_de').string) # Number of GHFamily hits
                worksheet.write(row, col, int(GHnum)) # Writes number of GH hits for that family
                GHnum = str(GHnum)
                print("Found " + GHnum + " annotations for GH" + GHfam + " in " + ArchList[i].string)
            orgnum = orgnum + 1
            
        


