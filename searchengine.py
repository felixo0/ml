#!/usr/bin/env python3
#Author@LogicWang
#2015.12.10
'''
this file include two class 
crawler to download,parse pages, and then save to database

'''

from urllib import request, parse
from bs4 import *

import re
import sqlite3
#the words to ignore
ignorewords=set(['the','of','to','and','a','in','is','it'])

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
        cur=self.con.execute("select rowid from %s where %s='%s'" %(table,field,value))
        res=cur.fetchone()
        if res==None:
            curs=self.con.execute("insert into %s (%s) values ('%s')" % (table,field,value))
            return curs.lastrowid
        else:
            return res[0]

    # Index an individual page
    def addtoindex(self,url,soup):
        if self.isindexed(url):
            return
        print('Indexing %s' %url)

        text=self.gettextonly(soup)
        words=self.separatewords(text)

        urlid=self.getentryid('urllist','url',url)

        for i  in range(len(words)):
            word=words[i]
            if word in ignorewords:
                continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) \
                    values (%d,%d,%d)" %(urlid,wordid,i))

    # Extract the text from an HTML page (no tags)
    def gettextonly(self,soup):
        v=soup.string
        if v==None:
            c = soup.contents
            resulttext=''
            for t in c:
                subtext=self.gettextonly(t)
                resulttext+=subtext+'\n'
            return resulttext
        else:
            return v.strip()

    # Separate the words by any non-whitespace character
    def separatewords(self,text):
        splitter=re.compile(r'\W*')
        return [s.lower() for s in splitter.split(text) if s!='']

    # Return true if this url is already indexed
    def isindexed(self,url):
        u=self.con.execute("select rowid from urllist where url='%s'" %url).fetchone()
        if u!=None:
            #double check
            v=self.con.execute('select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v!=None:
                return True
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

    # Create the database tables
    def createindextables(self):
        self.con.execute('create table urllist(url)')
        self.con.execute('create table wordlist(word)')
        self.con.execute('create table wordlocation(urlid,wordid,location)')
        self.con.execute('create table link(fromid integer,toid integer)')
        self.con.execute('create table linkwords(wordid,linkid)')
        self.con.execute('create index word_index on wordlist(word)')
        self.con.execute('create index url_index on urllist(url)')
        self.con.execute('create index word_url_index on wordlocation(wordid)')
        self.con.execute('create index urlto_index on link(toid)')
        self.con.execute('create index urlfrom_index on link(fromid)')
        self.dbcommit()

class searcher:
   #initial database
    def __init__(self,dbname):
        self.con=sqlite3.connect(dbname)

    def __del__(self): 
        self.con.close()

    def getmatchrows(self,q):
        #strings to build the query
        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]
        
        #split the words by sapces
        words=q.split(' ')
        tablenumber=0
        print(words)
        for word in words:
            wordrow=self.con.execute(\
                "select rowid from wordlist where word='%s'" %word).fetchone()
            if wordrow!=None:
                wordid=wordrow[0]
                wordids.append(wordid)
                if tablenumber>0:
                    tablelist+=','
                    clauselist+=' and '
                    clauselist+='w%d.urlid=w%d.urlid and ' %(tablenumber-1,tablenumber)
                fieldlist+=',w%d.location' %tablenumber
                tablelist+='wordlocation w%d' %tablenumber
                clauselist+='w%d.wordid=%d' %(tablenumber, wordid)
                tablenumber+=1
        #print(fieldlist,tablelist,clauselist)
        #create the query from the seprate parts
        fullquery='select %s from %s where %s' %(fieldlist,tablelist,clauselist)
        #fullquery='select * from %s' %(tablelist)
        print(fullquery)
        try:
            cur=self.con.execute(fullquery)
        except:
            rows=[]
            print('no search result')
        else:
            rows=[row for row in cur]

        return rows,wordids



