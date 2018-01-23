# -*- coding: utf-8 -*-

import os, re, paramiko, datetime, sys
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
        bSizer1 = wx.BoxSizer(wx.VERTICAL)
        m_staticText1 = wx.StaticText(panel, wx.ID_ANY, u"vROps IP:", wx.DefaultPosition, wx.DefaultSize, 0)
        m_staticText1.Wrap(-1)
        bSizer1.Add(m_staticText1, 0, wx.ALL, 10)


        self.text2 = wx.TextCtrl(panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.text2, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 10)

        self.m_staticText2 = wx.StaticText(panel, wx.ID_ANY, u"root's password", wx.DefaultPosition, wx.DefaultSize, 0)
        self.m_staticText2.Wrap(-1)
        bSizer1.Add(self.m_staticText2, 0, wx.ALL, 10)

        self.m_textCtrl3 = wx.TextCtrl(panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize,
                        wx.TE_PASSWORD|wx.TE_PROCESS_ENTER)
        bSizer1.Add(self.m_textCtrl3, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 10)
        self.m_textCtrl3.Bind(wx.EVT_TEXT_ENTER,self.OKbtn)

        m_button1 = wx.Button(panel, wx.ID_ANY, u"OK", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(m_button1, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 10)
        m_button1.Bind(wx.EVT_BUTTON,self.OKbtn)

        self.outtxt = wx.TextCtrl(panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, size=wx.Size(300,300), style = wx.TE_MULTILINE|wx.TE_READONLY)
        self.outtxt.SetBackgroundColour('#E8E8E8')
        bSizer1.Add(self.outtxt, 0, wx.ALL | wx.EXPAND | wx.ALIGN_CENTER_HORIZONTAL, 10)
        redir = Redirect(self.outtxt)
        sys.stdout = redir

        panel.SetSizer(bSizer1)
        self.Layout()
        self.Centre(wx.BOTH)

    def write(self,string):
        wx.CallAfter(self.outtxt, string)


    def errormsg(self):
        msgDialog = wx.MessageDialog(None, 'Error information!', 'msg', wx.YES_DEFAULT | wx.ICON_QUESTION)
        msgDialog.ShowModal()

    def OKbtn(self, event):
        self.sshdown()


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

    def sshdown(self):
        hostname = str(self.text2.GetValue())
        password = str(self.m_textCtrl3.GetValue())
        self.m_textCtrl3.Clear()
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
            ssh.connect(hostname, 22, username='root', password=password)
            sftp = ssh.open_sftp()
            files = sftp.listdir(remotepath)
            isExists = os.path.exists('./DownloadedRes/')
            if not isExists:
                os.makedirs('./DownloadedRes/')
            for f in files:
                if 'resource' in f:
                    if 'properties' in f:
                        print ''
                        #self.outtxt.SetLabel('--------------------------------------')
                        print '--------------------------------------'
                        print 'Beginning to download file  from %s  %s ' % (hostname, datetime.datetime.now())
                        print 'Downloading file:', os.path.join(remotepath, f)
                        sftp.get(os.path.join(remotepath, f), os.path.join(localpath, f))  # 下载
                        print 'Download file success %s ' % datetime.datetime.now()
                        print ''

            # sftp.get(remotepath, localpath)
            sftp.close()
            ssh.close()

            localfiles = os.listdir(localpath)
            for pro in localfiles:
                if '_' in pro:
                    relang = pro.replace('resources_', '')
                    relang2 = relang.replace('.properties', '')
                    fa = open(localpath + 'resources.properties')
                    a = fa.readlines()
                    fa.close()
                    fb = open(localpath + pro)
                    b = fb.readlines()
                    fb.close()
                    c = [i for i in a if i in b]
                    fc = open('test.txt', 'w')
                    fc.writelines(c)
                    fc.close()
                    isExists = os.path.exists('./result')
                    if not isExists:
                        os.makedirs('./result')
                    self.delblankline('test.txt', './result/' + relang2 + '.txt')
                    print 'identical files----/result/' + relang2 + '.txt' + '---created'
                    os.remove('test.txt')
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