# coding=utf-8

import os, re, paramiko, datetime, sys
import wx
import wx.xrc
from lxml import etree
import requests


class Redirect:
    def __init__(self, ctrl):
        self.out = ctrl

    def write(self, string):
        wx.CallAfter(self.out.AppendText, string)

class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"4K-Movie Torrents Download tool", pos=wx.DefaultPosition,size=wx.Size(400, 500), style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX)
        panel = wx.Panel(self)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        panel.SetBackgroundColour('#CAE1FF')
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        m_staticText1 = wx.StaticText(panel, wx.ID_ANY, u"请输入要下载的4K电影名:", wx.DefaultPosition, wx.DefaultSize, 0)
        m_staticText1.Wrap(-1)
        bSizer1.Add(m_staticText1, 0, wx.ALL, 10)


        self.text2 = wx.TextCtrl(panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER)
        self.text2.Bind(wx.EVT_TEXT_ENTER, self.OKbtn)
        bSizer1.Add(self.text2, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 10)


        m_button1 = wx.Button(panel, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        m_button1.Bind(wx.EVT_BUTTON,self.OKbtn)

        self.outtxt1 = wx.TextCtrl(panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(300,300), style = wx.TE_MULTILINE|wx.TE_READONLY)
        self.outtxt1.SetBackgroundColour('#E8E8E8')
        bSizer1.Add(self.outtxt1, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 10)
        redir = Redirect(self.outtxt1)
        sys.stdout = redir

        panel.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

    # def write(self,string):
    #     wx.CallAfter(self.outtxt1, string)

    def errormsg(self):
        msgDialog = wx.MessageDialog(None, 'Error information!', 'msg', wx.YES_DEFAULT | wx.ICON_QUESTION)
        msgDialog.ShowModal()

    def OKbtn(self, event):
        self.outtxt1.Clear()
        movie = str(self.text2.GetValue())
        url = 'https://www.zhaiiker.com/?s=%s' % movie
        self.search(movie,url)
        self.torrent(mainurl)

    def search(self,moviename,url):
        req = session.get(url, headers=headers)
        page = etree.HTML(req.text)
        resources = page.xpath(r'//a[contains(text(),"4K")]/../../../h2[@class="title"]/a')
        for resource in resources:
            urla = resource.get('href')
            mainurl.append(urla)


    def torrent(self,murl):
        for urla in murl:
            torrentreq = session.get(urla, headers=headers)
            torpage = etree.HTML(torrentreq.text)
            # img = torpage.xpath(r'//div[@class="post-image"]//img[contains(@class,"size-full")]')
            # imgurl = img[0].get('src')
            title = torpage.xpath(r'//div[@class="content"]/h1/text()')
            print title[0]
            torrenturls = torpage.xpath(r'//a[@rel="noopener"]')
            print '-----------------------------------------------------------------'
            print '-------------torrents and magnet urls-----------------'
            print '-----------------------------------------------------------------'
            for turl in torrenturls:
                print turl.get('href')
                print ''





session = requests.Session()
headers = {"User-Agent":"Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6",
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Connection':'keep-alive'
}
mainurl = []
torrentDownurl = []



if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show(True)
    # start the applications
    app.MainLoop()