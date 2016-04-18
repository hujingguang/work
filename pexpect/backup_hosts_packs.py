#!/bin/env python
import pexpect
import os
import commands
import time
Backup_Dir="/webdata/backup"
Host_Dict={'img':['backup_user@192.168.16.1','hello123'],
      }
Backup_Dict={
             'img':['/webdata/zabbix','/webdata/db_backup'], 
       }


if not os.path.exists(Backup_Dir):
    os.system('mkdir -p %s' %Backup_Dir)

def loopfun(pid):
    cmd=''' pstree -p|grep python|grep '%s' |grep rsync  ''' %pid
    while True:
        res=os.system(cmd)
        if res!=0:
            break
        else:
            time.sleep(5)
def backup():
    global Host_Dict,Backup_Dict,Backup_Dir
    for k,v in Host_Dict.iteritems():
        host,passwd=v[0],v[1]
        ip=host.split('@')[1]
        res,date=commands.getstatusoutput(''' date +"%Y-%m-%d %H:%M:%S" ''')
        host_backup_dir='%s/%s-%s' %(Backup_Dir,k,ip)
        if not os.path.exists(host_backup_dir):
            os.system('mkdir -p %s' %host_backup_dir)
        os.system('echo "%s" >>%s/backup.log' %(date,host_backup_dir))
        for point in Backup_Dict[k]:
            if point.endswith('/'):
                point=point.rstrip('/')
            cmd='''rsync -avlpq  %s:%s %s/ ''' %(host,point,host_backup_dir)
            os.system(r" echo '%s' >/tmp/.run.sh " %cmd)
            os.system(r" echo '%s' >>%s/backup.log" %(cmd,host_backup_dir))
            ch=pexpect.spawn('/bin/bash /tmp/.run.sh')
            res=ch.expect(['yes','assword:',pexpect.EOF,pexpect.TIMEOUT],timeout=120)
            if res == 0:
                ch.sendline('yes')
                ch.expect(['assword:',pexpect.EOF,pexpect.TIMEOUT],timeout=120)
                ch.sendline(passwd)
                loopfun(ch.pid)
                ch.close(force=True)
            elif res==1:
                ch.sendline(passwd)
                loopfun(ch.pid)
                ch.close(force=True)
            else:
                os.system(r"echo 'backup error' >>%s/backup.log" %host_backup_dir)


if __name__=='__main__':
    backup()

