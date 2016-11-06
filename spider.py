#coding:utf-8

import urllib2
from bs4 import BeautifulSoup,BeautifulStoneSoup
import os
import re
import time

def getPageDetail(href): #伪装成浏览器登陆,获取网页源代码
    headers = {  
        'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'  
    }  
    req = urllib2.Request(  
        url = href ,
        headers = headers  
    )
    try:
        post = urllib2.urlopen(req)
    except urllib2.HTTPError,e:
        print e.code
        print e.reason
    return post.read()

url = 'http://blog.csdn.net/experts.html'

def getExperts(url):
    uris = {}
    page = BeautifulSoup(getPageDetail(url),"html.parser")
    div = page.find('div',class_='cate_l')
    experts = div.find_all("a")
    for expert in experts:
        href="http://blog.csdn.net/peoplelist.html?channelid="+expert.get('id')+"&page=1"
        if href != "http://blog.csdn.net/experts.html":
            uris[expert.get_text()]=href
    return uris
#第一部分：得到首页博客专家各个系列链接

#===============================================================================
#得到每个类别所有专家的姓名和博客首页地址
def getAllExpert(href): 
    page=BeautifulSoup(getPageDetail(href),"html.parser")  #得到移动专家首页源代码，并beautifulsoup化
    for expert in page.find_all("a",class_="expert_name"):
        name = expert.get_text()
        href = expert.get("href")
        getBlog(name,href)
#第二部分：得到每类所有专家的姓名和首页链接

#===============================================================================
#获取当前专家个人博客所有博文的页数
def getPageNum(href):
    num =0
    page = getPageDetail(href)
    soup = BeautifulSoup(page,"html.parser")
    div = soup.find('div',class_='pagelist')
    
    if div:
        result = div.span.get_text().split(' ')
        list_num = re.findall("[0-9]{1}",result[3])
        for i in range(len(list_num)):
            num = num*10 + int(list_num[i]) #计算总的页数
        return num
    else:
        return 0

#获取每页所含博文的发布时间博文标题链接地址博文简介
#并储存至当前博客专家名称命名的文本文档中
def getText(name,url):
    page = BeautifulSoup(getPageDetail(url),"html.parser")
    spanlist = page.find_all("span",class_="link_title")
    postdate = page.find_all("span",class_="link_postdate")
    div_list = page.find_all("div",class_="article_description")
    k =0
    str1 = 'none'
    # 获取文章内容和内容
    for div in div_list:
        uri = spanlist[k].a.get("href").encode("utf-8")
        time = postdate[k].get_text().strip().encode("utf-8")
        title = spanlist[k].a.get_text().strip().encode("utf-8")
        detial = div.get_text().encode("utf-8")
        k+=1
        file = "article/"+name.encode("utf-8")+".txt"
        fp = open(file,"a")
        fp.write("标题:"+title+"\n时间:"+time+"\n链接:http://blog.csdn.net"+uri+"\n简介:"+detial+"\n")
        fp.write("-"*160+"\n")
        fp.close()

#获取博客专家下的每页博文链接
def getBlog(name,href):
    i =1
    start = time.time();
    for i in range(1,(getPageNum(href)+1)):
        url = href + '/article/list/' + str(i)
        getText(name,url)
        i+=1
    endof = time.time()-start
    print("=== CSDN博客专家：「 "+name.encode("utf-8")+" 」的个人博客采集完毕!累计耗时:%0.3fs"%(endof))
    
#第三部分：得到每类所有专家的博客内容链接
#===============================================================================


if __name__=="__main__":
    uris = getExperts(url)
    for uri_key,uri_val in uris.items():
        start = time.time()
        if uri_val != "http://blog.csdn.net/peoplelist.html?channelid=0&page=1":
            getAllExpert(uri_val)
            endof = time.time()-start
            print("<<< CSDN博客专家之：「 "+uri_key.encode("utf-8")+" 」专家相应博客 采集完毕 累计耗时：%0.3fs >>>"%(endof))
