import os
import pexpect


def put_pubkey(path,first,Log):
    f=open(path,'r')
    H=[]
    for line in f.readlines():
        hp=line.split(':')
        H.append(hp[0])
        if first:
            ch=pexpect.spawn('ssh-copy-id root@%s' %hp[0].strip())
            r=ch.expect(['password:',pexpect.EOF,pexpect.TIMEOUT])
            if r==0:
                ch.sendline(hp[1])
                ch.close(force=True)
            else:
                Log.write('the host:%s put pubkey failured \n' %hp[0])
        

    return H


