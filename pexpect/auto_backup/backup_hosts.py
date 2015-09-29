#!/usr/bin/python


import os
import pexpect
import logging
import commands
import re

ROOT_CONF_DIR='/data/rsyncback/service_conf'
RE_IP=re.compile(r'^192\.168\.16([89]?)\..*')
Services_Name=['nginx','mysql']


def parse_conf(root_dir):
    global RE_IP
    Service_Hosts={} 
    if not os.path.exists(root_dir):
        logging.error('the root_dir %s not exists!' %root_dir)
        exit(1)
    for sd in Services_Name:
        host_info={}
        ips=[]
        abs_conf=os.path.abspath(root_dir)+'/'+sd+'/'+'conf'
        if not os.path.exists(abs_conf):
            logging.error('the service conf file : %s  not exists!!' %abs_conf)
            exit(1)
        f=open(abs_conf,'r')
        for line in f.readlines():
            if line.startswith(sd):
                backup_dir=sd+'_dir'
                host_info[backup_dir]=line.split(':')[1].replace('\n','')
            else:
                line=line.strip()
                if RE_IP.match(line):
                    ips.append(line.replace('\n',''))
        host_info[sd]=ips
        Service_Hosts[sd]=host_info
    return Service_Hosts

def backup(path,hosts,service_name):
    has_pattern=False
    cmd=''
    pattern_path=''
    n=path.find('*')
    if n != -1:
        has_pattern=True
        pattern_path=path[:n+1]
    base_path=os.path.abspath(ROOT_CONF_DIR)+'/'+service_name
    hosts.reverse()
    for v in hosts:
        host,port,passwd=v.split(':')
        host=host.strip()
        port=port.strip()
        passwd=passwd.strip()
        local_path=base_path+'/'+host
        if not os.path.exists(local_path):
            os.system('mkdir -p %s' %local_path)
        if not has_pattern:
            cmd='rsync -zavl --delete %s:%s %s' %(host,path,local_path)
            logging.info(cmd)
            if os.path.exists('/tmp/tmp_shell'):
                os.system('rm -rf /tmp/tmp_shell')
            shell=open('/tmp/tmp_shell','w')
            shell.write(cmd+'\n')
            shell.close()
            new_cmd='bash /tmp/tmp_shell'
            ch=pexpect.spawn(new_cmd)
            res=ch.expect(['yes','assword:',pexpect.EOF],timeout=120)
            if res == 0:
                ch.sendline('yes')
                ch.sendline(passwd+'\n')
                ch.expect([']#',pexpect.EOF],timeout=180)
                ch.close()
            elif res == 1:
                ch.sendline(passwd+'\n')
                ch.expect([']#',pexpect.EOF],timeout=180)
                ch.close()
            else:
                logging.error('connect host: %s  failed!!' %host)
                ch.close()
        else:
            list_cmd=r'ssh %s "du -sh  %s" >/tmp/outputs ' %(host,pattern_path)
            logging.info('grep pattern dirs %s' %list_cmd)
            if os.path.exists('/tmp/tmp_shell.sh'):
                 os.system('rm -rf /tmp/tmp_shell.sh')
            shell=open('/tmp/tmp_shell.sh','w')
            shell.write(list_cmd+'\n')
            shell.close() 
            new_cmd='bash /tmp/tmp_shell.sh'
            ch=pexpect.spawn(new_cmd)
            res=ch.expect(['yes/no','assword:',pexpect.EOF],timeout=60)
            if res ==0:
                ch.sendline('yes')
                ch.sendline(passwd+'\n')
                ch.expect([']#',pexpect.EOF],timeout=120)
                ch.close()
            elif res==1:
                ch.sendline(passwd+'\n')
                ch.expect([']#',pexpect.EOF],timeout=120)
                ch.close()
            else:
                logging.error('connect host: %s faild for get mysql dir' %host)
                ch.close(force=True)
                continue
            if not os.path.exists('/tmp/outputs'):
                logging.error('/tmp/outputs not exists')
                exit(1)
            os.system(r"cat /tmp/outputs|awk '{print $2}' >/tmp/output")
            if not os.path.exists('/tmp/output'):
                logging.error('/tmp/output not exists')
                exit(1) 
            f=open('/tmp/output','r')
            for L in f.readlines():
                remote_dir=L.replace('\n','')
                p_n=remote_dir.rfind('/')
                s_dir=local_path+remote_dir[p_n:]
                if not os.path.exists(s_dir):
                    os.system('mkdir -p %s' %s_dir)
                remote_dir=remote_dir+path[n+1:]
                cmd='rsync -zavl --delete  %s:%s %s' %(host,remote_dir,s_dir)
                logging.info(cmd)
                shell=open('/tmp/tmp_shell','w')
                shell.write(cmd+'\n')
                shell.close()
                new_cmd='bash /tmp/tmp_shell'
                ch=pexpect.spawn(new_cmd)
                res=ch.expect(['assword:',pexpect.EOF],timeout=60)
                if res ==0:
                    ch.sendline(passwd+'\n')
                    ch.expect([']#',pexpect.EOF],timeout=120)
                    ch.close()
                else:
                    logging.error('run cmd: %s  failed !'%cmd)
                    ch.close(force=True)

def main():
    global ROOT_CONF_DIR,Services_Name
    if os.path.exists('/tmp/output'):
        os.system('rm -rf /tmp/output') 
    Sev_Dict=parse_conf(ROOT_CONF_DIR)
    for s in Services_Name:
        if s in Sev_Dict:
            hosts=Sev_Dict[s][s]
            path=Sev_Dict[s][s+'_dir']
            backup(path,hosts,s)


if __name__ == '__main__':
    main()



            

    

    



