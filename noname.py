# -*- coding: utf-8 -*-

import os, re, datetime, sys , glob
import wx
import wx.xrc

class Redirect:
    def __init__(self, ctrl):
        self.out = ctrl

    def write(self, string):
        wx.CallAfter(self.out.AppendText, string)



class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"SameReStrCheck", pos=wx.DefaultPosition,size=wx.Size(400, 500), style=wx.DEFAULT_FRAME_STYLE^wx.RESIZE_BORDER^wx.MAXIMIZE_BOX)
        panel = wx.Panel(self)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        panel.SetBackgroundColour('#CAE1FF')
        asize = wx.BoxSizer()
        self.opendir = wx.TextCtrl(panel)
        self.load = wx.Button(panel, label='打开文件夹...')
        self.load.Bind(wx.EVT_BUTTON,self.OnButton)

        asize.Add(self.opendir, 1, wx.EXPAND)
        asize.Add(self.load,0,wx.LEFT,5)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        bSizer1.Add(asize,0,wx.EXPAND|wx.ALL,10)

        m_button1 = wx.Button(panel, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)

        bSizer1.Add(m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        m_button1.Bind(wx.EVT_BUTTON,self.OKbtn)

        self.g1 = wx.Gauge(panel, range = 50, size = (350, 25), style = wx.GA_SMOOTH)
        bSizer1.Add(self.g1, 0, wx.ALL | wx.EXPAND, 10)


        self.outtxt = wx.TextCtrl(panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(300,350), style = wx.TE_MULTILINE|wx.TE_READONLY)
        self.outtxt.SetBackgroundColour('#E8E8E8')
        bSizer1.Add(self.outtxt, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 10)
        redir = Redirect(self.outtxt)
        sys.stdout = redir

        panel.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

    def wait(self):
        waitDialog = wx.MessageDialog(None, 'Wait a second...', 'msg', wx.YES_DEFAULT | wx.ICON_QUESTION)
        waitDialog.Show()

    def OnButton(self, event):
        """"""
        dlg = wx.DirDialog(self, u"选择文件夹", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            self.opendir.SetLabel(dlg.GetPath())  # 文件夹路径

        dlg.Destroy()

    def errormsg(self):
        msgDialog = wx.MessageDialog(None, 'Error information!', 'msg', wx.YES_DEFAULT | wx.ICON_QUESTION)
        msgDialog.ShowModal()

    def OKbtn(self, event):
        self.outtxt.Clear()
        self.g1.SetValue(0)
        self.g1.Pulse()
        self.compare()
        self.g1.SetValue(50)
        self.opendir.Clear()


    def delblankline(self,infile, outfile):
        infopen = open(infile, 'r')
        outfopen = open(outfile, 'w')
        lines = infopen.readlines()
        Dontneedtrans = ['vRealize Operations Manager', 'vRealize Air Operations', 'Log Insight', 'WenQuanYi Micro Hei',
                         'DejaVM Unicode', 'presentation.preview.lorem.ipsum', 'High Availability', 'product.copyright',
                         '{0}']
        for line in lines:
            if line.split():
                if not re.match(r'^#.*', line):
                    if all(string not in line for string in Dontneedtrans):
                        outfopen.writelines(line)
            else:
                outfopen.writelines("")
        infopen.close()
        outfopen.close()

    def compare(self):
        if os.path.exists('./result'):
            for dele in os.listdir('./result'):
                os.remove('./result' + '/' + dele)
        try:
            filepath = self.opendir.GetValue()
            for rt, dirs ,files in os.walk(filepath):
                for f in files:
                    if 'resources' in f:
                        # enf = open(rt + r'\resources.properties')
                        # ren = enf.readlines()
                        # enf.close()
                        isExists = os.path.exists('./result')
                        if not isExists:
                            os.makedirs('./result')
                        # fc = open('./result/en.txt', 'a+')
                        # fc.writelines(ren)
                        # fc.close()

                        relang = f.replace('resources_', '')
                        relang2 = relang.replace('.properties', '')
                        othf = open(rt + '\\' + f)
                        roth = othf.readlines()
                        othf.close()
                        fb = open('./result/'+relang2+'.txt', 'a+')
                        fb.writelines(roth)
                        fb.close()

            resultpath = './result'
            result = os.listdir(resultpath)

            for txt in result:
                if 'resources' not in txt:
                    lang = txt.replace('.txt', '')
                    ra = open('./result/resources.txt')
                    a = ra.readlines()
                    ra.close()
                    rb = open(resultpath + '/' + txt)
                    b = rb.readlines()
                    rb.close()
                    c = [i for i in a if i in b]
                    fc = open('test.txt', 'w')
                    fc.writelines(c)
                    fc.close()
                    self.delblankline('test.txt', './result/' + lang + '_Compare.txt')
                    print 'identical files----/result/' + lang + '_Compare.txt' + '---created'
                    os.remove(resultpath + '/' + txt)
            os.remove('./result/resources.txt')
            os.remove('test.txt')
            print 'Finished!'

            # for pro in localfiles:
            #     if '_' in pro:
            #         relang = pro.replace('resources_', '')
            #         relang2 = relang.replace('.properties', '')
            #         fa = open(localpath + 'resources.properties')
            #         a = fa.readlines()
            #         fa.close()
            #         fb = open(localpath + pro)
            #         b = fb.readlines()
            #         fb.close()
            #         c = [i for i in a if i in b]
            #         fc = open('test.txt', 'w')
            #         fc.writelines(c)
            #         fc.close()
            #         isExists = os.path.exists('./result')
            #         if not isExists:
            #             os.makedirs('./result')
            #         self.delblankline('test.txt', './result/' + relang2 + '.txt')
            #         print 'identical files----/result/' + relang2 + '.txt' + '---created'
            #         os.remove('test.txt')
        except:
            self.errormsg()






if __name__ == '__main__':
    localpath = './DownloadedRes/'
    remotepath = '/usr/lib/vmware-vcops/tomcat-web-app/webapps/ui/WEB-INF/classes/'

    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show(True)
    #start the applications
    app.MainLoop()