# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 17:38:05 2017

@author: Administrator
"""
import os
import xlwt
import re
import requests
from bs4 import BeautifulSoup
import time

headers = {
    'Host':'www.dianping.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3831.3 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cookie':'_lxsdk_cuid=15f9474ff11c8-0d51eb8a379c6c-4f541323-1fa400-15f9474ff12c8; _lxsdk=15f9474ff11c8-0d51eb8a379c6c-4f541323-1fa400-15f9474ff12c8; _hc.v=df9ef83c-6650-a002-e7ea-7e90fe6cc647.1510024217; __utma=1.237855090.1510024240.1510024240.1510024240.1; __utmz=1.1510024240.1.1.ut-mcsr=dianping.com|utmccn=(referral)|utmcmd=referral|utmcct=/shenzhen/food; _lx_utm=utm_source%3Ddianping.com%26utm_medium%3Dreferral%26utm_content%3D%252Fshenzhen%252Ffood; JSESSIONID=CEDADED56212961180FFBDF2FF3D6984; aburl=1; cy=7;cye=shenzhen; s_ViewType=10; _lxsdk_s=15f9f687be7-b0-484-8e8%7C%7C12'
    }
    
headers1 = {
    'Host':'www.dianping.com',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.3831.3 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cookie':'_lxsdk_cuid=15f9474ff11c8-0d51eb8a379c6c-4f541323-1fa400-15f9474ff12c8; _lxsdk=15f9474ff11c8-0d51eb8a379c6c-4f541323-1fa400-15f9474ff12c8; _hc.v=df9ef83c-6650-a002-e7ea-7e90fe6cc647.1510024217; __utma=1.237855090.1510024240.1510024240.1510024240.1; __utmz=1.1510024240.1.1.ut-mcsr=dianping.com|utmccn=(referral)|utmcmd=referral|utmcct=/shenzhen/food; _lx_utm=utm_source%3Ddianping.com%26utm_medium%3Dreferral%26utm_content%3D%252Fshenzhen%252Ffood; JSESSIONID=CEDADED56212961180FFBDF2FF3D6984; aburl=1; cy=7;cye=shenzhen; s_ViewType=10; _lxsdk_s=15f9f687be7-b0-484-8e8%7C%7C12'
    }    
    
    
shopid = []  
shopname = []
generalcomment = []
meanprice = []
shopcategory = []
address = []
reviewnum = []
taste = []
environment = []
service = []
coordinate = []

shop_name =[]
userID = []
times = []
starLevel = []
comments = []
tastes_  = []
circumstances = []
service_ = []


coorlist=[]
souptime=[]
key=[u"店名",u"类别",u"平均价格",u"地址",u"总评",u"口味",u"环境",u"服务",u"评价数目",u"纬度",u"经度"]    

def to_base36(value):  
    """将10进制整数转换为36进制字符串  
    """  
    if not isinstance(value, int):  
        raise TypeError("expected int, got %s: %r" % (value.__class__.__name__, value))  
  
    if value == 0:  
        return "0"  
  
    if value < 0:  
        sign = "-"  
        value = -value  
    else:  
        sign = ""  
  
    result = []  
  
    while value:  
        value, mod = divmod(value, 36)  
        result.append("0123456789abcdefghijklmnopqrstuvwxyz"[mod])  
  
    return sign + "".join(reversed(result))  
  
def decode(C):  
    """解析大众点评POI参数  
    """  
    digi = 16  
    add = 10  
    plus = 7  
    cha = 36  
    I = -1  
    H = 0  
    B = ''  
    J = len(C)  
    G = ord(C[-1])  
    C = C[:-1]  
    J -= 1  
      
    for E in range(J):  
        D = int(C[E], cha) - add  
        if D >= add:  
            D = D - plus  
        B += to_base36(D)  
        if D > H:  
            I = E  
            H = D  
  
    A = int(B[:I], digi)  
    F = int(B[I+1:], digi)  
    L = (A + F - int(G)) / 2  
    K = float(F - L) / 100000  
    L = float(L) / 100000  
    return {'lat': K, 'lng': L}


def get_infor():
    try:
        os.mkdir('data')
    except:
        print('--------')
    excel=xlwt.Workbook(encoding='utf-8')  
    sheet=excel.add_sheet('Sheet', cell_overwrite_ok=True)
    urls=['http://www.dianping.com/search/category/7/10/r1949p']
    for url in urls:
        page=1
        while page<=1:
            try:
                html=requests.get(url+str(page),headers=headers,timeout=30).text
            except:
                continue
            table=BeautifulSoup(html,'lxml').find('div',id='shop-all-list').find_all('li')
            #print(table)
            for li in table:
                try:
                    soup=li.find('div',attrs={'class':'txt'})
                    tit=soup.find('div',attrs={'class':'tit'})
                    comment=soup.find('div',attrs={'class':'comment'})
                    tag_addr=soup.find('div',attrs={'class':'tag-addr'})
                    shopid.append(tit.find('a').get('href')[-8:])
                    shopname.append(tit.find('a').get_text().replace('\r','').replace('\n',''))
                    generalcomment.append(comment.find('span').get('title'))
                    reviewnum.append(re.sub("\D", "",comment.find('a',attrs={'class':'review-num'}).get_text().replace('\r','').replace('\n','')))
                    meanprice.append(re.sub("\D", "",comment.find('a',attrs={'class':'mean-price'}).get_text().replace('\r','').replace('\n','')))
                    shopcategory.append(tag_addr.find('span',attrs={'class':'tag'}).get_text().replace('\r','').replace('\n',''))
                    address.append(tag_addr.find('span',attrs={'class':'addr'}).get_text().replace('\r','').replace('\n',''))
                    comment_list=soup.find('span',attrs={'class':'comment-list'}).find_all('span')
                    maps=li.find('div',attrs={'class':'operate J_operate Hide'})
                    coordinate.append(decode(maps.find_all('a')[2]['data-poi']))
                    #print(coordinate)
                    for i in comment_list:
                        text=i.get_text().replace('\r','').replace('\n','')
                        if text[:2] == u"口味":
                            taste.append(text[2:])
                        elif text[:2] ==u"环境":
                            environment.append(text[2:])
                        elif text[:2] ==u"服务":
                            service.append(text[2:])
                    
                except:
                    continue
            print("第",page,"页已经爬完")
            page+=1
            time.sleep(1)
    for i, col in enumerate(key):
        sheet.write(0,i,str(col))
    for i in range(len(shopname)):
        sheet.write(i+1,0,str(shopname[i]))
        sheet.write(i+1,1,str(shopcategory[i]))
        sheet.write(i+1,2,str(meanprice[i]))
        sheet.write(i+1,3,str(address[i]))
        sheet.write(i+1,4,str(generalcomment[i]))
        sheet.write(i+1,5,str(taste[i]))
        sheet.write(i+1,6,str(environment[i]))
        sheet.write(i+1,7,str(service[i]))
        sheet.write(i+1,8,str(reviewnum[i]))
        sheet.write(i+1,9,str(coordinate[i]["lat"]))
        sheet.write(i+1,10,str(coordinate[i]["lng"]))
    #excel.save('data/深圳.xls')
    

def get_comment():
    key_=[u'店名',u'用户ID',u'时间',u'总评价星级',u'口味',u'环境',u'服务',u'评价']
    excel=xlwt.Workbook(encoding='utf-8')  
    sheet=excel.add_sheet('Sheet', cell_overwrite_ok=True)
    url="http://www.dianping.com/shop/{}/review_all?pageno={}"
    pages = 1
    m=0
    for item in shopid:
        for page in range(pages):   
            m=m+1
            print(m)
            html=requests.get(url.format(item,str(page+1)),headers=headers).text
            #print(html)
            
            shop=BeautifulSoup(html,'lxml').find('a',{"href":"http://www.dianping.com/shop/{}".format(item)})
            if shop:
                
                table=BeautifulSoup(html,'lxml').find('div',{'class':'main'}).find_all('div',{'class':'content'})
                user_ids = BeautifulSoup(html,'lxml').find_all('div',{"class":"pic"})
                for userid in user_ids:
                    userID.append(userid.find_all('a')[0]["user-id"])
                for content in table:
                    times.append(content.find('span',attrs={'class':'time'}).get_text()[:5])
                    comments.append(content.find('div',attrs={'class':'J_brief-cont'}).get_text().replace(" ","").replace('\n',''))
                    soup=content.find('div',attrs={'class':'comment-rst'})
                    comment_list=soup.find_all('span')
                    starLevel.append(content.find_all("span")[0]["class"][-1][4:])
                    shop_name.append(shop.get_text())
                    for i in comment_list:
                        text=i.get_text()
                        if text[:2] ==u"口味":
                            tastes_.append(text[2])
                        elif  text[:2] ==u"环境":
                            circumstances.append(text[2])
                        elif  text[:2] ==u"服务":
                            service_.append(text[2])
            time.sleep(1)
    for i, col in enumerate(key_):
        sheet.write(0,i,str(col))
    for i in range(len(shop_name)):
        sheet.write(i+1,0,str(shop_name[i]))
        sheet.write(i+1,1,str(userID[i]))
        sheet.write(i+1,2,str(times[i]))
        sheet.write(i+1,3,str(starLevel[i]))
        sheet.write(i+1,4,str(tastes_[i]))
        sheet.write(i+1,5,str(circumstances[i]))
        sheet.write(i+1,6,str(service_[i]))
        sheet.write(i+1,7,str(comments[i]))
    #excel.save('data/评论.xls')

def get_member_comments():
    _key=[u'用户ID',u'时间',u'坐标']
    usrids=[]
    excel=xlwt.Workbook(encoding='utf-8')  
    sheet=excel.add_sheet('Sheet', cell_overwrite_ok=True)
    baseurl='http://www.dianping.com/member/{}/checkin'
    url="http://www.dianping.com/shop/{}"
    

    for usrid in userID[:9]:
        print(usrid)
        html=requests.get(baseurl.format(usrid),headers=headers).text
        #print(html)
        table=BeautifulSoup(html,'lxml').find('ul',id='J_list').find_all('li')
        
        for li in table:
            souptime.append(li.find('span',attrs={'class':'time'}).get_text()[:-1])
            shopID=li.find('a')["href"][6:]
            html=requests.get(url.format(shopID),headers=headers1).text
            shop=BeautifulSoup(html,'lxml').find_all("script")[10:12]
            shopGlat = re.compile(r'shopGlat: "(.*?)"')
            shopGlng = re.compile(r'shopGlng:"(.*?)"')
            lat=shopGlat.findall(str(shop))
            lng=shopGlng.findall(str(shop))
            usrids.append(usrid)
            if lat and lng:
                coorlist.append((lat[0],lng[0]))
            else:
                coorlist.append(('',''))
            print(coorlist)
    for i, col in enumerate(_key):
        sheet.write(0,i,str(col))
    for i in range(len(souptime)):
        sheet.write(i+1,0,str(usrids[i]))
        sheet.write(i+1,1,str(souptime[i]))
        sheet.write(i+1,2,str(coorlist[i]))
    excel.save('data/用户1.xls')   
    #print(coorlist)

if __name__ == '__main__':
    get_infor()
    get_comment()
    get_member_comments()
    #
    