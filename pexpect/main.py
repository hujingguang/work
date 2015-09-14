#!/usr/bin/env python
import pexpect
import os
from utils import put_pubkey


def main(script_path,putkey,first_put,hostfile):
    global Log
    if not os.path.exists(script_path):
        Log.write('script not exists!! %s \n' %script_path)
        Log.close()
        exit()
    n=script_path.rfind('/')
    script_name=script_path[n+1:]
    if putkey:
        if not os.path.exists(hostfile):
            print 'the host file %s not exists !!' %hostfile
            Log.write('the hostfile %s not exisits! \n' %hostfile)
            Log.close()
            exit()
        hosts=put_pubkey(hostfile,first_put,Log)
        for h in hosts:
            #pexpect.spawn('scp %s root@%s:/tmp' %(script_path,h))
            os.system('scp %s root@%s:/tmp' %(script_path,h))
            ch=pexpect.spawn('ssh root@%s ' %h,timeout=3)
            res=ch.expect(['#]',pexpect.EOF,pexpect.TIMEOUT])
            #if res != 0:
                #Log.write('ssh bad  connection about host: %s \n' %h)
                #continue
            ch.sendline('chmod +x /tmp/%s' %script_name)
            ch.expect(['#]',pexpect.EOF,pexpect.TIMEOUT]) 
            ch.sendline('nohup /tmp/%s &\n' %script_name)
            ch.close(force=True)
    else:
        if os.path.exists(hostfile):
            f=open(hostfile,'r')
            L=f.readlines()
            for line in L:
                hp=line.split(':')
                ch=pexpect.spawn('scp %s root@%s:/tmp' %(script_path,hp[0]))
                res=ch.expect(['assword:',pexpect.EOF,pexpect.TIMEOUT])
                if res !=0:
                    Log.write('put file to host: %s  failured \n' %hp[0])
                    ch.close(force=True)
                    continue
                ch.sendline(hp[1])
                ch=pexpect.spawn('ssh root@%s' %hp[0])
                res=ch.expect(['assword:',pexpect.EOF,pexpect.TIMEOUT])
                if res ==0:
                    ch.sendline(hp[1])
                    info=ch.expect([']#',pexpect.EOF,pexpect.TIMEOUT])
                    if info==0:
                        ch.sendline('nohup /tmp/%s &\n' %script_name)
                        ch.close(force=True)
                    else:
                        Log.write('nohup run failured !!\n')
                else:
                    Log.write('bad ssh connection for %s \n' %hp[0])
        else:
            Log.write('the hostfile: %s not exists!! \n' %hostfile)
            Log.close()
            exit()
    Log.close()

     


Script='/root/tmp/work/pexpect/test.sh'
Host_File='/root/tmp/work/pexpect/hosts'

global Log
Log=open('/tmp/python_run.log','a')


'''
   the var pubkey :  True express  put ssh pubkey to the client
   the var first:    False  express it has been  put the keys from server
'''
if __name__=='__main__':
    pubkey=True
    first=False
    main(Script,pubkey,first,Host_File)











