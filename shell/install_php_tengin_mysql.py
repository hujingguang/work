#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
__author__='Hoo'
SOFT_DIR="/webdata/opt/local"
PHP_Dir_Name="php5.6"
Mysql_Dir_Name='mysql2'
Tengine_Dir_Name="tengine2"
LOG_FILE="/tmp/install.log"
CentOS_Version="6"
PHP_Version="5.6.16"         #  the available version is: 5.6.16, 5.5.30, 5.4.40 
Tengine_Version="2.1.1"      # the available version is:   2.1.1
Jemalloc_Version="3.6.0"          # the available version is: 4.0.4, 3.6.0
PHP_Run_User="www"
Mysql_Run_User="mysql"
Tengine_Run_User="www"
Mysql_Version="5.6.10"       # the available version is : 5.6.10, 5.5.22
Mysql_DataDir=SOFT_DIR+"/"+Mysql_Dir_Name+"/data"
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
    cmd='''yum install gd-devel libxml2-devel curl-devel libpng-devel libjpeg-turbo-devel freetype-devel libmcrypt-devel libmcrypt php-mbstring mhash-devel libcurl-devel pcre-devel openssl-devel ncurses-devel bison-devel zlib-devel mysql-server -y &>/dev/null '''
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
    configure_args='''--prefix=%s/%s --enable-fpm --with-fpm-user=%s --with-fpm-group=%s --with-openssl --with-mcrypt --with-config-file-path=%s/php/etc --disable-ipv6 --with-pcre-regex --with-zlib --enable-calendar --enable-gd-native-ttf --with-freetype-dir --with-mysql --with-mysqli --with-pdo-mysql --enable-sockets --enable-soap --enable-mysqlnd --enable-mbstring ''' %(SOFT_DIR,PHP_Dir_Name,PHP_Run_User,PHP_Run_User,SOFT_DIR)
    cmd=''' cd /tmp/php-%s && ./configure %s &>/dev/null && make &>/dev/null  && make install &>/dev/null ''' %(PHP_Version,configure_args)
    res=os.system(cmd)
    if res !=0:
        os.system("echo 'make and make install failed' >%s" %LOG_FILE)
        exit()
    res=os.system(r"egrep '^%s' /etc/passwd &>/dev/null" %PHP_Run_User)
    if res!=0:
        os.system('useradd %s -s /sbin/nologin' %PHP_Run_User)
    os.system("cp %s/%s/etc/php-fpm.conf.default %s/%s/etc/php-fpm.conf " %(SOFT_DIR,PHP_Dir_Name,SOFT_DIR,PHP_Dir_Name))
    os.system("cp /tmp/php-%s/php.ini-production %s/%s/etc/php.ini" %(PHP_Version,SOFT_DIR,PHP_Dir_Name))
def compile_tengine():
    configure_args=''' --prefix=%s/%s --with-jemalloc --with-jemalloc=/tmp/jemalloc-%s --with-http_ssl_module --user=%s --group=%s --with-pcre --with-http_spdy_module --with-http_upstream_session_sticky_module=shared ''' %(SOFT_DIR,Tengine_Dir_Name,Jemalloc_Version,Tengine_Run_User,Tengine_Run_User)
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
    pid_dir=%s/%s/var/run
    . /etc/sysconfig/network
    . /etc/init.d/functions
    [ "$NETWORKING" = "no" ] && exit 0
    php_fpm="%s/%s/sbin/php-fpm"
    PHP_CONF_FILE=%s/%s/etc/php.ini
    prog=$(basename $php_fpm)
    lockfile=/var/lock/subsys/%s-fpm.lock
    php_fpm_pid="%s/%s/var/run/php-fpm.pid"
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
            #killproc -p $php_fpm_pid $prog -QUIT
            killall php-fpm
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
    ''' %(SOFT_DIR,PHP_Dir_Name,SOFT_DIR,PHP_Dir_Name,SOFT_DIR,PHP_Dir_Name,PHP_Dir_Name,SOFT_DIR,PHP_Dir_Name)

    nginx_script_contents=''' 
    #!/bin/bash
    . /etc/rc.d/init.d/functions
    . /etc/sysconfig/network
    [ "$NETWORKING" = "no" ] && exit 0
    nginx="%s/%s/sbin/nginx"
    prog=$(basename $nginx)
    NGINX_CONF_FILE="%s/%s/conf/nginx.conf"
    lockfile=/var/lock/subsys/nginx_%s.lock
    nginx_pid="%s/%s/logs/nginx.pid"
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
    ''' %(SOFT_DIR,Tengine_Dir_Name,SOFT_DIR,Tengine_Dir_Name,Tengine_Dir_Name,SOFT_DIR,Tengine_Dir_Name)
    php_script_name="/etc/init.d/%s-fpm" %PHP_Dir_Name
    tengine_script_name="/etc/init.d/%s" %Tengine_Dir_Name
    if not os.path.exists(php_script_name):
        php_fpm_script=open(php_script_name,"w")
        php_fpm_script.write(php_script_contents)
        php_fpm_script.close()
        res=os.system("chmod +x %s " %php_script_name)
        if res!=0:
            os.system("echo 'add php-fpm deamon failed ' >> /tmp/install.log")
    if not os.path.exists(tengine_script_name):
        nginx_script=open(tengine_script_name,"w")
        nginx_script.write(nginx_script_contents)
        nginx_script.close()
        res=os.system("chmod +x %s" %tengine_script_name)
        if res!=0:
            os.system("echo 'add nginx deamon faild ' >>/tmp/install.log ")


def install_mysql_independecy_packs():
    cmd=''' yum install ncurses-devel zlib-devel perl-DBI perl-DBD-mysql perl-Time-HiRes perl-IO-Socket-SSL perl-Term-ReadKey cmake -y &>/dev/null'''
    res=os.system(cmd)
    if res != 0:
        os.system("echo 'failed install mysql independency packs ' >/tmp/install.log")
        exit(1)

def compile_mysql():
    cmd='''wget http://web.wikiki.cn/mysql-%s.tar.gz &>/dev/null && mv mysql-%s.tar.gz /tmp && cd /tmp && tar -zxf mysql-%s.tar.gz ''' %(Mysql_Version,Mysql_Version,Mysql_Version)
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'get mysql source tarball failed ' >/tmp/install.log")
        exit(1)
    configure_args='''-DCMAKE_INSTALL_PREFIX=%s/%s -DMYSQL_DATADIR=%s -DSYSCONFIGDIR=%s/%s -DWITH_INNOBASE_STORAGE_ENGINE=1 -DWITH_MEMORY_STORAGE_ENGINE=1 -DWITH_MYISAM_STORAGE_ENGINE=1 -DWITH_ARCHIVE_STORAGE_ENGINE=1 -DWITH_READLINE=1 -DENABLED_LOCAL_INFILE=1 -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DEXTRA_CHARSET=utf8 -DWITH_USER=%s -DWITH_EMBEDDED_SERVER=OFF ''' %(SOFT_DIR,Mysql_Dir_Name,SOFT_DIR,SOFT_DIR,Mysql_Dir_Name,Mysql_Run_User)
    res=os.system("cd /tmp/mysql-%s && cmake %s &>/dev/null && make &>/dev/null && make install &>/dev/null" %(Mysql_Version,configure_args))
    if res!=0:
        os.system("echo 'compile mysql failed ' >/tmp/install.log ")
        exit(1)
    cmd='''cd /tmp/mysql-%s/support-files && cp mysql.server /etc/init.d/%s && sed -i 's#^basedir=#basedir=%s/%s#g' /etc/init.d/%s && sed -i 's#^datadir=#datadir=%s#g' /etc/init.d/%s ''' %(Mysql_Version,Mysql_Dir_Name,SOFT_DIR,Mysql_Dir_Name,Mysql_Dir_Name,Mysql_DataDir,Mysql_Dir_Name)
    res=os.system(cmd)
    if res!=0:
        os.system("echo 'add mysqld start scripts failed '>/tmp/install.log")
    res=os.system(r"egrep '^%s' /etc/passwd &>/dev/null" %Mysql_Run_User)
    if res!=0:
        os.system("useradd mysql -s /sbin/nologin")
    os.system("chown -R %s:%s %s/%s" %(Mysql_Run_User,Mysql_Run_User,SOFT_DIR,Mysql_Dir_Name))
    init_db_cmd='''%s/%s/scripts/mysql_install_db --user=%s --basedir=%s/%s --datadir=%s ''' %(SOFT_DIR,Mysql_Dir_Name,Mysql_Run_User,SOFT_DIR,Mysql_Dir_Name,Mysql_DataDir)
    print Mysql_DataDir
    cmd=''' rm -rf %s/* ''' %Mysql_DataDir
    os.system(cmd)
    if not os.path.exists("%s/mysql/user.MYD" %Mysql_DataDir):
        os.system("chown -R %s:%s %s" %(Mysql_Run_User,Mysql_Run_User,Mysql_DataDir))
        res=os.system(init_db_cmd)
        if res!=0:
            os.system(r"rm -rf %s/*" %Mysql_DataDir)
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
    if not os.path.exists('%s/%s' %(SOFT_DIR,PHP_Dir_Name)):
        compile_php()
    if not os.path.exists('%s/%s' %(SOFT_DIR,Tengine_Dir_Name)):
        compile_tengine()
    print "Ok .....  php and tengine is installed "
    generate_deamon_scripts()
    if not os.path.exists('%s/%s' %(SOFT_DIR,Mysql_Dir_Name)):
        install_mysql_independecy_packs()
        compile_mysql()
    os.system("rm -rf /tmp/php-%s && rm -rf /tmp/tengine-%s && rm -rf /tmp/mysql-%s" %(PHP_Version,Tengine_Version,Mysql_Version))
if __name__=="__main__":
    start_install()



