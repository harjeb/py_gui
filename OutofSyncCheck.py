#-*- coding: utf-8 -*-
import os, datetime, re, sys
import paramiko

def delblankline(infile,outfile):
    infopen = open(infile,'r')
    outfopen = open(outfile,'w')
    lines = infopen.readlines()
    Dontneedtrans = ['vRealize Operations Manager','vRealize Air Operations','Log Insight','WenQuanYi Micro Hei','DejaVM Unicode','presentation.preview.lorem.ipsum','High Availability','product.copyright','{0}']
    for line in lines:
        if line.split():
            if not re.match(r'^#.*',line):
                if all(string not in line for string in Dontneedtrans):
                    outfopen.writelines(line)
        else:
            outfopen.writelines("")
    infopen.close()
    outfopen.close()

def checkResource():
    refiles = os.listdir(localpath)
    resources = ['fr','es','de','ko','resources.properties']
    for i in refiles:
        if all(string not in i for string in resources):
            print i
            return True

def sshdown():
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
                    print '--------------------------------------'
                    print 'Beginning to download file  from %s  %s ' % (hostname, datetime.datetime.now())
                    print 'Downloading file:', os.path.join(remotepath, f)
                    sftp.get(os.path.join(remotepath, f), os.path.join(localpath, f))  # 下载
                    print 'Download file success %s ' % datetime.datetime.now()
                    print ''

        # sftp.get(remotepath, localpath)
        sftp.close()
        ssh.close()
    except:
        print 'Check whether server has opened ssh'
        raw_input('Press Enter to exit...')
        sys.exit()

localpath = './DownloadedRes/'
remotepath = '/usr/lib/vmware-vcops/tomcat-web-app/webapps/ui/WEB-INF/classes/'
#hostname = '172.16.189.46'
hostname = raw_input("Please input the vROps IP(need opened ssh):")
password = raw_input("Please input root's password:")
sshdown()
localfiles = os.listdir(localpath)
for pro in localfiles:
    if '_' in pro:
        relang = pro.replace('resources_', '')
        relang2 = relang.replace('.properties', '')
        fa = open(localpath+'resources.properties')
        a = fa.readlines()
        fa.close()
        fb = open(localpath+pro)
        b = fb.readlines()
        fb.close()
        c = [i for i in a if i in b]
        fc = open('test.txt', 'w')
        fc.writelines(c)
        fc.close()
        isExists = os.path.exists('./result')
        if not isExists:
            os.makedirs('./result')
        delblankline('test.txt','./result/'+relang2+'.txt')
        print 'identical files----' + relang2 + '.txt' +'---created'
        os.remove('test.txt')

raw_input('Press Enter to exit...')