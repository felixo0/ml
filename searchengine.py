#!/usr/bin/env python3
#Author@LogicWang
#2015.12.10
'''
this file include two class 
crawler to download,parse pages, and then save to database

'''

from urllib import request, parse
from bs4 import *

import sqlite3
#the words to ignore
ignoreword=set(['the','of','to','and','a','in','is','it'])

class crawler:
    def __init__(self,dbname='search.db'):
        self.con=sqlite3.connect(dbname)
    def __del__(self):
        self.con.close()
    def dbcommit(self):
        self.con.commit()

    # Auxilliary function for getting an entry id and adding
    # it if it's not present
    def getentryid(self,table,field,value,createnew=True):
        return None
    # Index an individual page
    def addtoindex(self,url,soup):
        print('Indexing %s' %url)
    # Extract the text from an HTML page (no tags)
    def gettextonly(self,soup):
        return None
    # Separate the words by any non-whitespace character
    def separatewords(self,text):
        return None
    # Return true if this url is already indexed
    def isindexed(self,url):
        return False
    # Add a link between two pages
    def addlinkref(self,urlFrom,urlTo,linkText):
        pass
    # Starting with a list of pages, do a breadth
    # first search to the given depth, indexing pages
    # as we go
    def crawl(self,pages,depth=2):
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    c = request.urlopen(page)
                except:
                    print("Could not open %s" %page)
                    continue
                soup=BeautifulSoup(c.read())
                self.addtoindex(page,soup)

                links = soup('a')
                for link in links:
                    if('href' in dict(link.attrs)):
                        url=parse.urljoin(page,link['href'])
                        if url.find("'")!=-1:
                            continue
                        url=url.split('#')[0]
                        if url[0:4]=='http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText=self.gettextonly(link)
                        self.addlinkref(page,url,linkText)
            self.dbcommit()
            pages=newpages
        pass
    # Create the database tables
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute
