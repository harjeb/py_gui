# coding=utf-8
import urllib, re, time, random
from lxml import etree
import requests
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
from selenium.webdriver.common.by import By
from pytesser import *
from urllib import urlretrieve




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



def rarbg2(imdbtt):
    driver = webdriver.PhantomJS(executable_path=r'D:\pygui\bt\phantomjs-2.1.1-windows\bin\phantomjs.exe')
    for tt in imdbtt:
        driver.get('http://rarbg.is/torrents.php?search=%s' % tt)
        time.sleep(random.randint(5, 7))
        driver.save_screenshot('1.png')
        #WebDriverWait(driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, "//a[text()='Click here']")))
        try:
            clickhere = driver.find_element_by_xpath("//a[text()='Click here']")
            clickhere.click()
        except:
            pass
        time.sleep(random.randint(2,4))
        driver.save_screenshot('2.png')
        WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.XPATH,"//img[contains(@src,'captcha2')]")))
        img = driver.find_element_by_xpath("//img[contains(@src,'captcha2')]")
        imgurl = img.get_attribute('src')
        driver.save_screenshot('3.png')
        urlretrieve(imgurl,'readimg.png')

        image = Image.open('readimg.png')
        print image_to_string(image)
        print imgurl
        #driver.save_screenshot('3.png')
        #driver.save_screenshot(tt+'.png')
        #searchresult = driver.find_element_by_xpath('//tr[@class="lista2"]//td[2]/a[1]')
        #print searchresult



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
    rarbg2(imdbtt)
    print btdownPage


