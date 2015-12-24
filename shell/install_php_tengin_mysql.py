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
Mysql_Version="5.6.10"       # the available version is : 5.6.10, 5.5.22
Mysql_DataDir=SOFT_DIR+"/mysql/data"
def check_network():
    res=os.system("ping -c 1 -i 1 120.24.239.32 &>/dev/null")
    if res !=0:
        os.system("echo 'network is unabled' >%s" %LOG_FILE)
        exit(1)
    res=os.system("nslookup www.baidu.com &>/dev/null")
    if res!=0:
        os.system("echo 'nameserver  223.5.5.5\nnameserver 112.124.47.27 ' >>/etc/resolv.conf")
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
    configure_args='''--prefix=%s/php --enable-fpm --with-fpm-user=%s --with-fpm-group=%s --with-config-file-path=%s/php/etc --disable-ipv6 --with-pcre-regex --with-zlib --enable-calendar --enable-gd-native-ttf --with-freetype-dir --with-mysql --with-mysqli --with-pdo-mysql --enable-sockets --enable-soap --enable-mysqlnd --enable-mbstring ''' %(SOFT_DIR,PHP_Run_User,PHP_Run_User,SOFT_DIR)
    cmd=''' cd /tmp/php-%s && ./configure %s &>/dev/null && make &>/dev/null  && make install &>/dev/null ''' %(PHP_Version,configure_args)
    res=os.system(cmd)
    if res !=0:
        os.system("echo 'make and make install failed' >%s" %LOG_FILE)
        exit()
    res=os.system(r"egrep '^%s' /etc/passwd &>/dev/null" %PHP_Run_User)
    if res!=0:
        os.system('useradd %s -s /sbin/nologin' %PHP_Run_User)
    os.system("cp %s/php/etc/php-fpm.conf.default %s/php/etc/php-fpm.conf " %(SOFT_DIR,SOFT_DIR))
    os.system("cp /tmp/php-%s/php.ini-production %s/php/etc/php.ini" %(PHP_Version,SOFT_DIR))
def compile_tengine():
    configure_args=''' --prefix=%s/tengine --with-jemalloc --with-jemalloc=/tmp/jemalloc-%s --with-http_ssl_module --user=%s --group=%s --with-pcre --with-http_spdy_module --with-http_upstream_session_sticky_module=shared ''' %(SOFT_DIR,Jemalloc_Version,Tengine_Run_User,Tengine_Run_User)
    cmd=''' wget http://web.wikiki.cn/jemalloc-%s.tar.bz2 &>/dev/null && mv jemalloc-%s.tar.bz2 /tmp && cd /tmp && tar -xjf jemalloc-%s.tar.bz2 ''' %(Jemalloc_Version,Jemalloc_Version,Jemalloc_Version)
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'install jemalloc failed ' >/tmp/install.log")
        exit()
    cmd='''wget http://web.wikiki.cn/tengine-%s.tar.gz &>/dev/null&& mv tengine-%s.tar.gz /tmp && cd /tmp && tar -zxf tengine-%s.tar.gz ''' %(Tengine_Version,Tengine_Version,Tengine_Version)
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'get tengine source failed ' >/tmp/install.log")
        exit()
    cmd=''' cd /tmp/tengine-%s && ./configure %s &>/dev/null && make &>/dev/null && make install &>/dev/null ''' %(Tengine_Version,configure_args)
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'compile tengine failed '>/tmp/install.log")
        exit()
    res=os.system(r"egrep '^%s' /etc/passwd &>/dev/null" %Tengine_Run_User)
    if res!=0:
        os.system('useradd %s -s /sbin/nologin' %Tengine_Run_User)


def generate_deamon_scripts():
    php_script_contents=''' 
    #!/bin/bash
    PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin
    export PATH
    pid_dir=%s/php/var/run
    . /etc/sysconfig/network
    . /etc/init.d/functions
    [ "$NETWORKING" = "no" ] && exit 0
    php_fpm="%s/php/sbin/php-fpm"
    PHP_CONF_FILE=%s/php/etc/php.ini
    prog=$(basename $php_fpm)
    lockfile=/var/lock/subsys/php-fpm.lock
    php_fpm_pid="%s/php/var/run/php-fpm.pid"
    ulimit -SHn 65535 
    start() {
            [ -x $php_fpm ] || exit 1
            [ -f $PHP_CONF_FILE ] || exit 2
            echo -n $"Starting $prog: "
            daemon --pidfile $php_fpm_pid $php_fpm -c $PHP_CONF_FILE
            retval=$?
            [ $retval -eq 0 ] && touch $lockfile
            return $retval
            }
    php_fpm_status() {
            status -p $php_fpm_pid $prog
            }
    stop() {
            echo -n $"Stopping $prog: "
            killproc -p $php_fpm_pid $prog -QUIT
            sleep 5
            retval=$?
            echo
            [ $retval -eq 0 ] && rm -f $lockfile
            return $retval
            }
    restart() {
            stop
            start
            }
    case "$1" in
    start)
    start
    ;;
    stop)
    stop
    ;;
    restart)
    restart
    ;;
    status)
    php_fpm_status
    ;;
    *)
    echo $"Usage: $0 {start|stop|status|restart}"
    exit 2
    esac
    ''' %(SOFT_DIR,SOFT_DIR,SOFT_DIR,SOFT_DIR)

    nginx_script_contents=''' 
    #!/bin/bash
    . /etc/rc.d/init.d/functions
    . /etc/sysconfig/network
    [ "$NETWORKING" = "no" ] && exit 0
    nginx="%s/tengine/sbin/nginx"
    prog=$(basename $nginx)
    NGINX_CONF_FILE="%s/tengine/conf/nginx.conf"
    lockfile=/var/lock/subsys/nginx.lock
    nginx_pid="%s/tengine/logs/nginx.pid"
    start() {
    [ -x $nginx ] || exit 5
    [ -f $NGINX_CONF_FILE ] || exit 6
    echo -n $"Starting $prog: "
    daemon --pidfile $nginx_pid $nginx -c $NGINX_CONF_FILE
    retval=$?
    [ $retval -eq 0 ] && touch $lockfile
    return $retval
    }
    stop() {
    echo -n $"Stopping $prog: "
    killproc -p $nginx_pid $prog
    retval=$?
    [ $retval -eq 0 ] && rm -f $lockfile
    return $retval
    }
    restart() {
    stop
    start
    }
    reload() {
    echo -n $"Reloading $prog: "
    $nginx -s reload
    RETVAL=$?
    return $RETVAL
    }
    nginx_status() {
    status $prog
    }
    case "$1" in
    start)
    start
    ;;
    stop)
    stop
    ;;
    restart)
    restart
    ;;
    reload)
    reload
    ;;
    status)
    nginx_status
    ;;
    *)
    echo $"Usage: $0 {start|stop|status|restart|reload}"
    exit 2
    esac
    ''' %(SOFT_DIR,SOFT_DIR,SOFT_DIR)

    if not os.path.exists("/etc/init.d/php-fpm"):
        php_fpm_script=open("/etc/init.d/php-fpm","w")
        php_fpm_script.write(php_script_contents)
        php_fpm_script.close()
        res=os.system("chmod +x /etc/init.d/php-fpm ")
        if res!=0:
            os.system("echo 'add php-fpm deamon failed ' >> /tmp/install.log")
    if not os.path.exists("/etc/init.d/nginx"):
        nginx_script=open("/etc/init.d/nginx","w")
        nginx_script.write(nginx_script_contents)
        nginx_script.close()
        res=os.system("chmod +x /etc/init.d/nginx ")
        if res!=0:
            os.system("echo 'add nginx deamon faild ' >>/tmp/install.log ")


def install_mysql_independecy_packs():
    cmd=''' yum install cmake  ncurses-devel zlib-devel perl-DBI perl-DBD-mysql perl-Time-HiRes perl-IO-Socket-SSL perl-Term-ReadKey -y &>/dev/null'''
    res=os.system(cmd)
    if res !=0:
        os.system("echo 'failed install mysql independency packs ' >/tmp/install.log")
        exit(1)

def compile_mysql():
    cmd='''wget http://web.wikiki.cn/mysql-%s.tar.gz &>/dev/null && mv mysql-%s.tar.gz /tmp && cd /tmp && tar -zxf mysql-%s.tar.gz ''' %(Mysql_Version,Mysql_Version,Mysql_Version)
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'get mysql source tarball failed ' >/tmp/install.log")
        exit(1)
    configure_args='''-DCMAKE_INSTALL_PREFIX=%s/mysql -DMYSQL_DATADIR=%s -DSYSCONFIGDIR=%s/mysql -DWITH_INNOBASE_STORAGE_ENGINE=1 -DWITH_MEMORY_STORAGE_ENGINE=1 -DWITH_MYISAM_STORAGE_ENGINE=1 -DWITH_ARCHIVE_STORAGE_ENGINE=1 -DWITH_READLINE=1 -DENABLED_LOCAL_INFILE=1 -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DEXTRA_CHARSET=utf8 -DWITH_USER=mysql -DWITH_EMBEDDED_SERVER=OFF ''' %(SOFT_DIR,SOFT_DIR,SOFT_DIR)
    res=os.system("cd /tmp/mysql-%s && cmake %s && make && make install" %(Mysql_Version,configure_args))
    if res!=0:
        os.system("echo 'compile mysql failed ' >/tmp/install.log ")
        exit(1)
    cmd='''cd /tmp/mysql-%s/support-files && cp mysql.server /etc/init.d/mysqld && sed -i 's#^basedir=#basedir=%s/mysql#g' /etc/init.d/mysqld && sed -i 's#^datadir=#datadir=%s#g' /etc/init.d/mysqld ''' %(Mysql_Version,SOFT_DIR,Mysql_DataDir)
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'add mysqld start scripts failed '>/tmp/install.log")
    os.system("chown -R %s:%s %s/mysql" %(Mysql_Run_User,Mysql_Run_User))
    init_db_cmd='''%s/mysql/scripts/mysql_install_db --user=%s --basedir=%s/mysql --datadir=%s ''' %(SOFT_DIR,Mysql_Run_User,SOFT_DIR,Mysql_DataDir)
    res=os.system(init_db_cmd)
    if res!=0:
        os.system("rm -rf /var/lib/mysql && rm -rf %s/*" %Mysql_DataDir)
        res=os.system(init_db_cmd)
        if res!=0:
            os.system("echo 'init mysql db failed ' >/tmp/install.log")
            exit(1)
    print 'Ok....... compile mysql source success ! '
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
    generate_deamon_scripts()
    if not os.path.exists('%s/mysql' %SOFT_DIR):
        compile_mysql()
if __name__=="__main__":
    start_install()



