#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
__author__='Hoo'
SOFT_DIR="/webdata/opt/local"
LOG_FILE="/tmp/install.log"
CentOS_Version="6"
PHP_Version="5.4.40"         #  the available version is: 5.6.16, 5.5.30, 5.4.40 
Tengine_Version="2.1.1"      # the available version is:   2.1.1
Jemalloc_Version="3.6.0"          # the available version is: 4.0.4, 3.6.0
PHP_Run_User="www"
Tengine_Run_User="www"
def check_network():
    res=os.system("ping -c 1 -i 1 www.baidu.com &>/dev/null")
    if res !=0:
        os.system("echo 'network is unabled' >%s" %LOG_FILE)
    res=os.system("nslookup www.baidu.com &>/dev/null")
    if res!=0:
        os.system("echo 'nameserver 8.8.8.8 ' >>/etc/resolv.conf")
def install_epel():
    res=os.system('rpm -qa|grep epel &>/dev/null')
    if res !=0:
        s=os.system("wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-%s.noarch.rpm &>/dev/null && rpm -ivh epel-release-latest-%s.noarch.rpm &>/dev/null" %(CentOS_Version,CentOS_Version))
        if s !=0:
            os.system("echo 'failed to install epel '>%s" %LOG_FILE)
            exit()
    
def install_compile_env():
    cmd='''yum install gcc gcc-c++ cmake make -y &>/dev/null '''
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'failed to install gcc compile enviroment' >%s" %LOG_FILE)
        exit()
def install_dependency_packs():
    cmd='''yum install gd-devel libxml2-devel curl-devel libpng-devel libjpeg-turbo-devel freetype-devel php-mbstring mhash-devel libcurl-devel pcre-devel openssl-devel ncurses-devel bison-devel zlib-devel mysql-server -y &>/dev/null '''
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'failed to install php dependency_packs >%s'" %LOG_FILE)
        exit()
    
def compile_php():
    tar_name="php-%s.tar.gz" %PHP_Version
    cmd='''wget http://web.wikiki.cn/%s &>/dev/null && mv %s /tmp && cd /tmp && tar -xzf %s ''' %(tar_name,tar_name,tar_name)
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'get php source tarbar failed' >%s" %LOG_FILE)
        exit()
    configure_args='''--prefix=%s/php --enable-fpm --with-fpm-user=%s --with-fpm-group=www --with-config-file-path=/webdata/opt/local/php/etc --disable-ipv6 --with-pcre-regex --with-zlib --enable-calendar --enable-gd-native-ttf --with-freetype-dir --with-mysql --with-mysqli --with-pdo-mysql --enable-sockets --enable-soap --enable-mysqlnd --enable-mbstring ''' %(SOFT_DIR,PHP_Run_User)
    cmd=''' cd /tmp/php-%s && ./configure %s &>/dev/null && make &>/dev/null  && make install &>/dev/null ''' %(PHP_Version,configure_args)
    res=os.system(cmd)
    if res !=0:
        os.system("echo 'make and make install failed' >%s" %LOG_FILE)
        exit()
    res=os.system(r"egrep '^%s' /etc/passwd" %PHP_Run_User)
    if res!=0:
        os.system('useradd %s -s /sbin/nologin' %PHP_Run_User)

def compile_tengine():
    configure_args=''' --prefix=%s/tengine --with-jemalloc --with-jemalloc=/tmp/jemalloc-%s --with-http_ssl_module --user=%s --group=%s --with-pcre --with-http_spdy_module --with-http_upstream_session_sticky_module=shared ''' %(SOFT_DIR,Jemalloc_Version,Tengine_Run_User,Tengine_Run_User)
    cmd=''' wget http://web.wikiki.cn/jemalloc-%s.tar.bz2 &>/dev/null && mv jemalloc-%s.tar.bz2 /tmp && cd /tmp && tar -xjf jemalloc-%s.tar.bz2 ''' %(Jemalloc_Version,Jemalloc_Version,Jemalloc_Version)
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'install jemalloc failed ' >/tmp/install.log")
        exit()
    cmd='''wget http://tengine.taobao.org/download/tengine-%s.tar.gz &>/dev/null&& mv tengine-%s.tar.gz /tmp && cd /tmp && tar -zxf tengine-%s.tar.gz ''' %(Tengine_Version,Tengine_Version,Tengine_Version)
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'get tengine source failed ' >/tmp/install.log")
        exit()
    cmd=''' cd /tmp/tengine-%s && ./configure %s &>/dev/null && make &>/dev/null && make install &>/dev/null ''' %(Tengine_Version,configure_args)
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'compile tengine failed '>/tmp/install.log")
        exit()
    res=os.system(r"egrep '^%s' /etc/passwd " %Tengine_Run_User)
    if res!=0:
        os.system('useradd %s -s /sbin/nologin' %Tengine_Run_User)

def start_install():
    check_network()
    install_epel()
    res=os.system("which gcc &>/dev/null && which g++ &>/dev/null && which make &>/dev/null ")
    if res!=0:
        install_compile_env()
    install_dependency_packs()
    if not os.path.exists('%s/php' %SOFT_DIR):
        compile_php()
    if not os.path.exists('%s/tengine' %SOFT_DIR):
        compile_tengine()
    print "Ok .....  php and tengine is installed "

if __name__=="__main__":
    start_install()



