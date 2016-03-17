
Python_Prefix=/usr/local/python2.7
mkdir -p /tmp/install_dir
/bin/mv /usr/bin/python /usr/bin/python.bak && /bin/rm -f /usr/bin/python
cd /tmp/install_dir 
wget 10.117.74.247:8080/Python-2.7.10.tgz &>/dev/null
wget 10.117.74.247:8080/setuptools-18.4.tar.gz &>/dev/null
wget 10.117.74.247:8080/pip-7.1.2.tar.gz &>/dev/null
grep '/usr/bin/python2.6' /usr/bin/yum
if [ $? != 0 ]
then
sed -i 's#^\#!/usr/bin/python#\#!/usr/bin/python2.6#' /usr/bin/yum
tar -zxf Python-2.7.10.tgz && cd Python-2.7.10 && ./configure --prefix=$Python_Prefix &>/dev/null && make &>/dev/null && make install &>/dev/null
/bin/ln -s ${Python_Prefix}/bin/python /usr/bin/python
cd /tmp/install_dir && tar -zxf setuptools-18.4.tar.gz && cd setuptools-18.4 && /usr/bin/python setup.py install &>/dev/null
cd /tmp/install_dir && tar -zxf pip-7.1.2.tar.gz && cd pip-7.1.2 && /usr/bin/python setup.py install &>/dev/null
cd ~
fi
if [ ! -e /usr/bin/python.bak ]
then
    /bin/mv /usr/bin/python /usr/bin/python.bak
    /bin/rm -f /usr/bin/python
    /bin/ln -L ${Python_Prefix}/bin/python2.7 /usr/bin/python
fi
echo 'PATH=.:$PATH:'${Python_Prefix}'/bin' >>/etc/profile
echo 'export PATH' >>/etc/profile
source /etc/profile
pip install Jinja2 &>/dev/null
PATH=.:$PATH:${Python_Prefix}/bin
export PATH
pip install --upgrade pip &>/dev/null
yum install salt-ssh salt salt-minion -y &>/dev/null
chkconfig --level 12345 salt-minion on 
if [ ! -e /etc/salt/minion.d/master.conf ]
then
mkdir -p /etc/salt/minion.d
/bin/touch /etc/salt/minion.d/master.conf
echo 'master: 10.117.74.247' >>/etc/salt/minion.d/master.conf
echo 'id: '`hostname` >>/etc/salt/minion.d/master.conf
fi
service salt-minion start
/bin/rm -rf /tmp/install_dir
/bin/rm -f `pwd`/$0
