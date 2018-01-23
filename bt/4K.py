# coding=utf-8
import urllib, re, time, random
from lxml import etree
import requests
from selenium import webdriver

def search(moviename):
    req = session.get(url, headers=headers)
    page = etree.HTML(req.text)
    resources = page.xpath(r'//a[contains(text(),"4K")]/../../../h2[@class="title"]/a')
    for resource in resources:
        urla = resource.get('href')
        mainurl.append(urla)


def torrent(murl):
    for urla in murl:
        torrentreq = session.get(urla, headers=headers)
        torpage = etree.HTML(torrentreq.text)
        # img = torpage.xpath(r'//div[@class="post-image"]//img[contains(@class,"size-full")]')
        # imgurl = img[0].get('src')
        title = torpage.xpath(r'//div[@class="content"]/h1/text()')
        #titlename = title[0].get('text()')
        print title
        torrenturls = torpage.xpath(r'//a[@rel="noopener"]')
        for turl in torrenturls:
            print '--------------------------------------------------------------------------------------------------------'
            print '-----------------------------------torrents and magnet urls---------------------------------------------'
            print '--------------------------------------------------------------------------------------------------------'
            print turl.get('href')





session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive'
}

if __name__ == '__main__':
    mainurl = []
    torrentDownurl = []
    movie = raw_input("请输入电影名:")
    url = 'https://www.zhaiiker.com/?s=%s' % movie
    search(movie)
    torrent(mainurl)
