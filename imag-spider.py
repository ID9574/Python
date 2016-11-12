# -*- coding: utf-8 -*-
import urllib
import urllib2
import time
import os
import hashlib
import random
from urlparse import urlparse
from bs4 import BeautifulSoup

def setUserAgent():
	userAgent=(
		'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
		'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
	)
	return userAgent[random.randint(0,len(userAgent)-1)]


def getResponse(uri):
	headers={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'deflate, sdch',
		'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'User-Agent':setUserAgent()
	}

	request=urllib2.Request(
		url = uri,
		headers = headers
	)

	try:
		response = urllib2.urlopen(request)
	except Exception as e:
		print(e.code)
		print(e.reason)
   
	return response.read()

def md5(code_str):
	decode = hashlib.md5()
	if isinstance(code_str,str):
		decode.update(code_str)
		return decode.hexdigest()
def generate_file_name(name="",suffix=""):
	suffix_list = ('.bmp','.jpg','.jpeg','.png','.gif')
	if not suffix in suffix_list:
		suffix='.jpeg'
	if name == "":
		name=md5(str(int(time.time())+random.randint(1111,9999)))

	return name+suffix


def downloadImg(html):
    result = BeautifulSoup(html,"html.parser")
    imglist = result.findAll("img")
    
    #定义文件夹的名字
    t = time.localtime(time.time())
    foldername = time.strftime("%Y-%m-%d",t)
    picpath = 'images/%s' % (foldername) #下载到的本地目录

    if not os.path.exists(picpath):   #路径不存在时创建一个
        os.makedirs(picpath)   
    x = 0
    for imgurl in imglist:
    	image = imgurl.get("src")
    	suffix =os.path.splitext(os.path.basename(image))[1]
        target = picpath+'/%s'%(generate_file_name(suffix=suffix))
        print("Downloading image to location from: [ "+image+" ]")
        try:
        	urllib.urlretrieve(image, target)
        	x+=1
        except Exception as e:
        	print(e)
        	pass

    return {"total":len(image),"success":x}

    
    
if __name__ == '__main__':
    print '''            *************************************
            **    Welcome to use SpiderImage   **
            **     Created on  2016-11-12      **
            **       @author: ID9574           **
            *************************************'''

    html = getResponse("http://www.nipic.com/index.html")
    image=downloadImg(html)
    overstr = "Download has finished. A total of %s pic, Successfully downloaded %s pic of %s pic failed."
    print(overstr%(image['total'],image['success'],(image['total']-image['success'])))
