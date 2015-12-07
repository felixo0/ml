import feedparser
import re

def getwordcounts(url):
    wc={}
    #for url in urls:
    #    d=feedparser.parse(url)
    d=feedparser.parse(url)
    words=getwords(d.feed.summary)
    for word in words:
        wc.setdefault(word,0)
        wc[word]+=1
    return url,wc

def getwords(html):
    #remove all the html tag
    txt=re.compile(r'<[^>]+>').sub('',html)
    
    #split words by all non-alpha characters
    words=re.compile(r'[^A-Z^a-z]+').split(txt)
    return [word.lower() for word in words if word!='']

apcount={}
wordcounts={}
for feedurl in open('feedlist.txt'):
    title,wc=getwordcounts(feedurl)
    wordcounts[title]=wc
    for word,count in wc.items():
        apcount.setdefault(word,0)
        if count>1:
            apcount[word]+=1

wordlist=[]
for w,bc in apcount.items():
    frac=float(bc)/len(wordcounts)
    if frac>0.1 and frac<0.5:
        wordlist.append(w)

out=open('blogdata.txt','w')
out.write('Blog')
for word in wordlist:
    out.write('\t%s' %word)
out.write('\n')
for blog,wc in wordcounts.items():
    blog=re.compile(r'[\n]+').sub('',blog)
    out.write('%s' %blog)
    for word in wordlist:
        if word in wc:
            out.write('\t %d' % wc[word])
        else:
            out.write('\t0')
    out.write('\n')

