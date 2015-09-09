import os
import pexpect

def put_pubkey(path):
    f=open(path,'r')
    for line in f.readlines():
        hp=line.split(':')
        ch=pexpect.spawn('ssh-copy-id root@%s' %hp[0].strip())
        r=ch.expect(['password:',pexpect.EOF,pexpect.TIMEOUT])
        if r==0:
            ch.sendline(hp[1])
            ch.close(force=True)
