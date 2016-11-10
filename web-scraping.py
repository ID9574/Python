#coding:utf-8

import os
import re
import time
import urllib,urllib2
from bs4 import BeautifulSoup,BeautifulStoneSoup


def setRequest(uri):
	headers={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Encoding':'deflate, sdch',
		'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
	}
	request=urllib2.Request(
		url = uri,
		headers = headers
	)
	
	try:
		response = urllib2.urlopen(request)
	except urllib2.HTTPError,e:
		print(e.code)
		print(e.reason)

	return response.read()

def getImages(response):
	print("-"*10+"开始下载文章中的图片"+"-"*10)
	imglist = []
	images = response.findAll("img")
	if len(images) > 0:
		start = time.time();
		localpath = "images/%s"%(time.strftime("%Y%m%d",time.localtime(time.time())))
		if not os.path.exists(localpath):
			os.makedirs(localpath)
		for img in images:
			uri = img.get("src")
			image = localpath+"/"+os.path.basename(uri)
			if not os.path.exists(image):
				try:
					urllib.urlretrieve(uri,image)
				except Exception as e:
					print(e)
			else:
				print("the file already exist!")
			imglist.append({"ouri":uri,"nuri":"../"+image})
		overt = time.strftime("%S",time.localtime(time.time()-start))
		print("-"*10+"共下载「"+str(len(imglist))+"」张图片 总耗时「"+str(overt)+"」秒"+"-"*10)
		return imglist
	else:
		return None
	
def getResponse(response):
	result = BeautifulSoup(response,"html.parser")
	title  = result.find("span",class_="link_title").a.get_text().strip().encode("utf-8").replace("\r\n","")
	detail = result.find("div",{"id":"article_content","class":"article_content"})
	imguris=getImages(detail)
	if isinstance(imguris,list):
		detail = detail.encode("utf-8")
		for uris in imguris:
			if isinstance(uris,dict) and uris['ouri'] != "":
				detail = detail.replace(uris['ouri'].encode("utf-8"),uris['nuri'].encode("utf-8"))
	else:
		detail  = detail.encode("utf-8")

	file_name = time.strftime("%Y%m%d%H%I%M%S",time.localtime(time.time()))
	article = "article/%s.html"%(file_name)
	file   	= open(article,"a")
	file.write(detail)
	file.close()


if __name__ == '__main__':
	response = setRequest("http://blog.csdn.net/zouyee/article/details/50532765")
	getResponse(response)