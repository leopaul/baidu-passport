#!/usr/bin/env python
#coding: utf-8
#file   : passport.py
#author : ning
#date   : 2013-05-28 18:55:28


import urllib, urllib2
import os, sys
import re, time
import logging

PWD = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(PWD, './lib/'))

from pcl import httpc
from pcl.common import *

logger = logging.getLogger('pyhttpclient')
#init_logging(logger, logging.DEBUG)

c = httpc.HttplibHTTPC()
#c = httpc.CurlHTTPC()

USERNAME = 'idning@gmail.com'
PASS = 'idning123456'

headers = {}

def dtoken():
    global headers
    resp = c.get('https://passport.baidu.com/v2/?login')
    bduss = resp['header']['set-cookie']
    headers = {'Cookie': bduss}
    
    resp = c.get('https://passport.baidu.com/v2/api/?getapi&tpl=pp&apiver=v3&tt=1369737464654&class=login', headers)
    print resp['body']
    resp = json_decode(resp['body'])
    return resp['data']['token']
    
def login():
    global headers
    token = dtoken()
    postdata = {
        'charset':'UTF-8',
        'token': token,
        'tpl':'pp',
        'apiver':'v3',
        #'tt': (int)(time.time()*1000),
        'tt': 1369737464654,
        'codestring':'',
        'isPhone':False,
        'safeflg':0,
        #'staticpage':'https://passport.baidu.com/v3Jump.html',
        #'u':'https://passport.baidu.com/',
        'username': USERNAME, 
        'password': PASS,
        'verifycode':'',
        'mem_pass':'on',
        'ppui_logintime':5519,
        'callback':'parent.bd__pcbs__ngvtnr',
    }
    body = urllib.urlencode(postdata)
    #body += '&staticpage=https://passport.baidu.com/v3Jump.html&u=http://passport.baidu.com/center?_t=1369737446'

    print body
    print headers
    print '-'*50

    headers['Content-Type'] =  'application/x-www-form-urlencoded'

    #headers = {'Cookie': 'BAIDUID=1724A7C3A1BC605412B81C1E216E1860:FG=1;'}
    #body = 'staticpage=https://passport.baidu.com/v3Jump.html&charset=UTF-8&token=07372f13147deb7b7fc0b0b3b589fb73&tpl=pp&apiver=v3&tt=1369741698146&codestring=&isPhone=false&safeflg=0&u=https://passport.baidu.com/&username=idning@gmail.com&password=idning000&verifycode=&mem_pass=on&ppui_logintime=160054&callback=parent.bd__pcbs__rn1nqm'
    #print body
    #print headers

    resp = c.post('https://passport.baidu.com/v2/api/?login', body, headers)
    print resp
    cookie = resp['header']['set-cookie']
    cookie = cookie.split(';')
    cookie = [a.split('=') for a in cookie]
    print cookie
    
    cookie = dict(cookie)
    return cookie['BDUSS']

def list_video(bduss):
    header = {'Cookie': 'BDUSS=%s;'%bduss}
    resp = c.get('http://pan.baidu.com/api/categorylist?channel=chunlei&clienttype=0&web=1&category=1&pri=-1&num=100&t=1369744741142&page=1&_=1369744741144', header)
    return json_decode(resp['body'])['info']

def main():
    bduss = login()
    print bduss
    lst = list_video(bduss)
    for v in lst:
        print v['server_filename']
        print v['dlink']
        print '---------'

if __name__ == "__main__":
    main()

