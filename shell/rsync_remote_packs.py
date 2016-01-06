#!/bin/env python
import pexpect
import os
import commands
import time
Backup_Dir="/webdata/backup"
Host_Dict={'web1':['root@121.41.76.121','password'],
           'web2':['root@121.40.173.23','password']
      }
Backup_Dict={'web1':['/etc/init.d/log_roate.sh','/var/spool/cron/root','/webdata/opt/local/php','/etc/init.d/zabbix_agentd','/soft/zabbix','/webdata/opt/local/sersync','/webdata/conf','/webdata/webdir/liquan','/etc/rc.local','/etc/sysconfig/iptables','/webdata/opt/local/tengine/conf/nginx.conf'],
             'web2':['/etc/init.d/log_roate.sh','/var/spool/cron/root','/webdata/opt/local/php','/etc/init.d/zabbix_agentd','/soft/zabbix','/webdata/opt/local/sersync','/webdata/conf','/etc/rc.local','/etc/sysconfig/iptables','/webdata/opt/local/tengine/conf/nginx.conf'],
       }


if not os.path.exists(Backup_Dir):
    os.system('mkdir -p %s' %Backup_Dir)

def loopfun():
    while True:
        res=os.system('pstree|grep rsync &>/dev/null')
        if res!=0:
            break
        else:
            time.sleep(10)
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
            cmd='''rsync -avlpq --delete %s:%s %s/ ''' %(host,point,host_backup_dir)
            os.system(r" echo '%s' >/tmp/.run.sh " %cmd)
            os.system(r" echo '%s' >>%s/backup.log" %(cmd,host_backup_dir))
            ch=pexpect.spawn('/bin/bash /tmp/.run.sh')
            res=ch.expect(['yes','assword:',pexpect.EOF,pexpect.TIMEOUT],timeout=120)
            if res == 0:
                ch.sendline('yes')
                ch.sendline(passwd+'\n')
                loopfun()
                ch.close(force=True)
            elif res==1:
                ch.sendline(passwd+'\n')
                loopfun()
                ch.close(force=True)
            else:
                os.system(r"echo 'backup error' >>%s/backup.log" %host_backup_dir)


if __name__=='__main__':
    backup()

