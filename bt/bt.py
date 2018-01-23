# coding=utf-8
import urllib, re, time, random
from lxml import etree
import requests
from selenium import webdriver

def mvnames(list):
    for url in list:
        req = session.get(url, headers=headers)
        page = etree.HTML(req.text)
        hrefs = page.xpath('//div[@id="star-rating-widget"]')
        for href in hrefs:
            movienames.append(href.get('data-title'))

def rarbg(imdbTT):
    for tt in imdbTT:
        rarurl = 'http://rarbg.is/torrents.php?search=%s' % tt
        rarreq = session.get(rarurl, headers=headers)
        rarpage = etree.HTML(rarreq.text)
        bturls = rarpage.xpath('//tr[@class="lista2"]//td[2]/a[1]')
        for bt in bturls:
            btdownPage.append('rarbg.is' + bt.get('href'))
        time.sleep(random.randint(2, 5))
        rarreq.close()





session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive'
}


if __name__ == '__main__':
    imdbtt = []
    movienames = []
    btdownPage = []
    cnmovie = raw_input("请输入电影名:")
    fmurl = 'http://dianying.fm/search/?text=%s' % cnmovie
    fmreq = session.get(fmurl, headers=headers)
    fmpage = etree.HTML(fmreq.text)
    fmtitle = fmpage.xpath('//a[@class="fm-orange"]')
    for t in fmtitle:
        tt = t.get('href').replace('http://www.imdb.com/title/','')
        ttx = tt.replace('/','')
        imdbtt.append(ttx)

    #imdburl = 'http://www.imdb.com/title/tt3348730/'
    rarbg(imdbtt)
    print btdownPage


