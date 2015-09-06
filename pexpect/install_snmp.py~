#!/usr/bin/env python
import pexpect,sys


def up_script(ip,passwd):
    ch=pexpect.spawn('scp /etc/snmp/snmpd.conf root@%s:/etc/snmp/' %ip)
    ch.logfile=sys.stdout
    index=ch.expect(['(yes/no)','assword:',pexpect.EOF,pexpect.TIMEOUT])
    if index==0:
        ch.sendline('yes\n')
    ch.sendline(passwd)
    index=ch.expect(['Permission',']#',pexpect.EOF,pexpect.TIMEOUT])
    if index==0:
        print 'scp failure password is error'
    ch.close(force=True)

def run_script(ip,passwd,user):
    ch=pexpect.spawn('ssh %s@%s' %(user,ip))
    ch.logfile=sys.stdout
    index=ch.expect(['(yes/no)','assword:',pexpect.EOF,pexpect.TIMEOUT])
    if index==0:
        ch.sendline('yes\n')
    ch.sendline(passwd)
    index=ch.expect(['Permission',']#',pexpect.EOF,pexpect.TIMEOUT])
    if index==0:
        print 'password is error'
        ch.close(force=True)
    ch.sendline('chmod 777 /root/tmp/test.sh')
    ch.expect([']#',pexpect.EOF,pexpect.TIMEOUT])
    ch.sendline('nohup /root/tmp/test.sh\n')
    ch.close(force=True)

if __name__=='__main__':
    run_script('wikiki.cn','Hu5340864','root')
