#!/usr/bin/env python
import pexpect,sys

Log=open('/tmp/installsnmp.log','w')

def up_script(ip,passwd):
    ch=pexpect.spawn('scp /etc/snmp/snmpd.conf root@%s:/etc/snmp/' %ip)
    ch.logfile=Log
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
    ch.logfile=Log
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
    Log.close()

def put_pubkey():
    f=open('hosts','r')
    for line in f.readlines():
        l=line.split(':')
        ch=pexpect.spawn('ssh-copy-id root@%s' %l[0].strip())
        r=ch.expect(['password:',pexpect.EOF,pexpect.TIMEOUT])
        if r==0:
            ch.sendline(l[1])
            ch.close(force=True)


        

if __name__=='__main__':
    #run_script('wikiki.cn',passwd,'root')
    put_pubkey()
