import os,commands
Log=open('/tmp/init_system.log','a')

def epel():
    res=os.system('wget http://mirrors.sohu.com/fedora-epel/epel-release-latest-6.noarch.rpm -P /tmp -o /tmp/installsnmp.log')
    if res!=0:
        Log.write('Get EPEL Error !!! ')
        Log.close()
        exit()
    res=os.system('rpm -ivh /tmp/epel-release-latest-6.noarch.rpm &>/tmp/installsnmp.log')
    if res!=0:
        Log.write('Install EPEL Error !!!')
        Log.close()
        exit()
    os.system('yum makecache &>/dev/null')

def configure_env():
    res=os.system(r'yum -y install ncurses-devel gcc* &>/dev/null')
    if res != 0:
        Log.write('Install gcc* Error !!!')
        Log.close()
        exit()
    res=os.system(r'yum -y install openssl-devel libstdc++* libxml2-devel libpng-devel zlib-devel bzip2-devel libjpeg-devel freetype-devel  curl-devel dnsmasq libaprutil-1.so.0 apr* expect libssl.so.10 libstdc++.so.6')
    if res !=0:
        Log.write('Install Error! ')
        Log.close()
        exit()

def load_kernel_mod():
    res,info=commands.getstatusoutput('modprobe bridge && modprobe ip_conntrack')
    if res != 0:
        Log.write('load_kernel_mod Error %s' %info)
        Log.close()
        exit()
    f=open('/etc/rc.local','a')
    contents="modprobe ip_conntrack\nmodprobe bridge\n"
    f.write(contents)
    f.close()

def  optimize_kernel():
    contents="net.ipv4.tcp_keepalive_time = 1200\nnet.ipv4.tcp_keepalive_intvl = 30\nnet.ipv4.tcp_keepalive_probes = 3\nnet.netfilter.nf_conntrack_max = 655360000\nnet.nf_conntrack_max = 655360000\nnet.netfilter.nf_conntrack_tcp_timeout_established =1200\nnet.ipv4.ip_local_port_range = 1024 65000\nnet.ipv4.tcp_max_tw_buckets = 5000\n"
    f=open('/etc/sysctl.conf','a')
    f.write(contents)
    f.close()
    f=open('/etc/profile','a')
    f.write('ulimit -u 102400\nulimit -n 65535\n')
    f.close()

def close_useless_server():
    os.system('chkconfig  postfix off && chkconfig atd off && chkconfig auditd off && chkconfig cups off')
    os.system('chkconfig ip6tables off && chkconfig nfslock off && chkconfig rpcgssd off')

def main():
    res=os.system('rpm -qa|grep epel')
    if res != 0:
        epel()
    configure_env()
    res=os.system('grep "modprobe bridge" /etc/rc.local')
    if res != 0:
        optimize_kernel()
    res=os.system('grep "ulimit -n" /etc/profile')
    if res!=0:
        load_kernel_mod()
    close_useless_server()
    Log.write('Init system successed !! ')
    Log.close()

if __name__ == '__main__':
    main()
    






