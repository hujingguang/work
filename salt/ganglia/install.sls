
configure_rrd_env:
  pkg.installed:
   - pkgs:
     - gcc
     - pango
     - pango-devel
     - pangomm
     - pangomm-devel
     - libxml2
     - libxml2-devel


up_rrdtool:
  file.managed:
    - name: /tmp/rrdtool-1.4.6.tar.gz
    - source: salt://ganglia/files/rrdtool-1.4.6.tar.gz
  cmd.run:
    - cwd: /tmp
    - name: tar -zxvf rrdtool-1.4.6.tar.gz
    - require:
      - file: /tmp/rrdtool-1.4.6.tar.gz
install_rrdtool:
  cmd.run:
    - name: cd /tmp/rrdtool-1.4.6 && ./configure --prefix=/usr/local/rrdtool && make && make install
    - require:
      - pkg: configure_rrd_env
      - cmd: up_rrdtool
    - unless: test -d /usr/local/rrdtool

configure_ganglia_env:
  pkg.installed:
   - pkgs:
     - pcre
     - pcre-devel
     - apr-devel
     - apr
     - expat
     - expat-devel
     - libconfuse
     - libconfuse-devel

up_ganglia:
  file.managed:
   - name: /tmp/ganglia-3.7.2.tar.gz
   - source: salt://ganglia/files/ganglia-3.7.2.tar.gz

unzip_ganglia:
  cmd.run:
   - cwd: /tmp
   - name: tar -zxvf ganglia-3.7.2.tar.gz && mkdir -p /etc/ganglia
   - require:
     - file: up_ganglia

install_ganglia:
  cmd.run:
    - name: cd /tmp/ganglia-3.7.2 && ./configure --prefix=/soft/ganglia --enable-perl --enable-status --with-zlib  --enable-python --with-librrd=/usr/local/rrdtool --with-php --with-libapr --enable-php --with-libpcre && make && make install
    - require:
      - cmd: unzip_ganglia
      - pkg: configure_ganglia_env
    - unless: test -d /soft/ganglia

up_scripts:
  file.managed:
   - name: /etc/ganglia/gmond.conf
   - source: salt://ganglia/files/gmond.conf

up_server_scripts:
  file.managed:
   - name: /etc/init.d/gmond 
   - source: salt://ganglia/files/gmond
   - mode: 755

start_gmond:
  cmd.run:
   - name: chkconfig --add gmond
   - unless: chkconfig --list gmond
  service.running:
    - name: gmond
    - enable: True
    - watch:
      - file: up_server_scripts
  
bind_ip:
  cmd.run:
    - name: ip route add 239.2.11.71 dev eth1 

