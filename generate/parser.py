#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib, urllib2,sys,re
from multiprocessing import Pool
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17',
    'Accept-Charset':'utf-8'}

def partparse(names):
    for name in names:
        try:
            parse(name)
        except:
            continue

def parse(name):
    count=0
    req = urllib2.Request("http://vk.com/%s"%name,None, headers)
    f = urllib2.urlopen(req).read()
    if not f:
        return
    try:
        uid=re.search("href=\"\/photo(\d+)_\d+\"",f).group(1)
        req = urllib2.Request("http://vk.com/album%s_0"%uid,None, headers)
        f = urllib2.urlopen(req).read()
        photos=re.findall("href=\"(\/photo\d+_\d+)\"",f)
        for photo in photos:
            req = urllib2.Request("http://vk.com%s"%photo,None, headers)
            p=urllib2.urlopen(req).read()
            pictures=re.findall("y_src\":\"([\w\W]+?.jpg)\"",p)
            if len(pictures)==0:
                print "\033[01;33mUser %s hasn't any avatars\033[00;00m" % name
                return
            for pic in pictures:
                pic=pic.replace("\/","/")
                req = urllib2.Request(pic,None,headers)
                picname=re.search(r"/([\w\-_]+?.jpg)",pic).group(1)
                f=urllib2.urlopen(req).read()
                try:
                    pict=open("../pictures/%s"%picname)
                    pict.close()
                except:
                    pict=open("../pictures/%s"%picname,"wb")
                    pict.write(f)
                    pict.close()
                    count+=1
            print "\033[01;32m%s has %d photos\033[00;00m"%(name,count)
    except:
        print "\033[01;31m%s called exception\033[00;00m" % name
        return

allnames=list(set([s.strip() for s in open("names.txt").readlines()]))
a=len(allnames)
names=[allnames[0:a/4],allnames[a/4:a/2],allnames[a/2:a*3/4],allnames[a*3/4:]]
pool=Pool(4)
pool.map(partparse,names)

