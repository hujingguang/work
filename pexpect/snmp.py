#!/usr/bin/env python

import os,commands

def epel():
    res=os.system('wget http://mirrors.sohu.com/fedora-epel/epel-release-latest-6.noarch.rpm -P /tmp -o /tmp/installsnmp.log')
    if res!=0:
        os.system('echo get epel error >>/tmp/installsnmp.log')
        exit()
    res=os.system('rpm -ivh /tmp/epel-release-latest-6.noarch.rpm &>/tmp/installsnmp.log')
    if res!=0:
        os.system('echo install epel error >>/tmp/installsnmp.log')
        exit()
    os.system('yum makecache &>/dev/null')
    res=os.system('yum install net-snmp net-snmp-utils -y &>/tmp/installsnmp.log')
    if res!=0:
        exit()
def snmp_conf():
    f=open('/etc/snmp/snmpd.conf','w')
    content='com2sec notConfigUser  192.168.168.0/24    careland\ncom2sec notConfigUser  192.168.169.0/24    careland\ncom2sec notConfigUser  default    careland\ngroup   notConfigGroup v1           notConfigUser\ngroup   notConfigGroup v2c notConfigUser\nview    systemview    included   .1.3.6.1.2.1.1\nview    systemview    included   .1.3.6.1.2.1.25.1.1\naccess  notConfigGroup ""      any       noauth    exact  all none none\nview all    included  .1\nsyslocation Unknown (edit /etc/snmp/snmpd.conf)\nsyscontact Root <root@localhost> (configure /etc/snmp/snmp.local.conf)\ndontLogTCPWrappersConnects yes\n'
    f.write(content)
    f.close()
def start_snmp():
    r=os.system('rpm -qa|grep epel')
    if r!=0:
        epel()
    snmp_conf()
    res=os.system('service snmpd start &>/tmp/installsnmp.log')

if __name__=='__main__':
    res=os.system('rpm -qa|grep net-snmp$')
    if res!=0:
        start_snmp()

        




    

