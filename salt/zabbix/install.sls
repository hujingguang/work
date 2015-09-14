{% set tar_name = 'zabbix-2.2.10.tar.gz' %}
{% set decompress_dir = 'zabbix-2.2.10' %}
{% set zabbix_dir = '/soft/zabbix' %}
{% set mysql_dir = '/soft/mysql' %}
{% set server = '192.168.61.159' %}

{% set server_active='192.168.61.159:10050' %}

{% set configure_args= '--prefix=%s --enable-proxy --enable-agent --enable-ipv6 --with-mysql=%s/bin/mysql_config  --with-libxml2 --with-net-snmp --with-libcurl' %(zabbix_dir,mysql_dir)  %}


add_user:
  user.present:
    - name: zabbix
    - shell: /sbin/nologin
    - system: True
    - gid_from_name: True
    - createhome: False

uptar:
  file.managed:
    - name: /tmp/{{ tar_name }}
    - source: salt://zabbix/files/pkg/{{ tar_name }}

unzip:
  cmd.run:
   - cwd: /tmp
   - name: tar -xzf {{ tar_name }}
   - require:
     - file: uptar
   - unless: test -d /tmp/{{ decompress_dir }}

depend_pkgs:
  pkg.installed:
   - pkgs:
     - libxml2
     - libxml2-devel
     - gcc
     - net-snmp
     - net-snmp-devel
     - libcurl-devel

install_zabbix:
  cmd.run:
   - name: cd /tmp/{{ decompress_dir }} && ./configure {{ configure_args }} && make && make install
   - require:
     - cmd: unzip
   - unless: test -d {{ zabbix_dir }}

zabbix_conf:
  file.managed:
    - name: {{ zabbix_dir }}/etc/zabbix_agentd.conf
    - source: salt://zabbix/files/zabbix_agent/zabbix_agentd.conf
    - template: jinja
    - defaults:
        server: {{ server }}
        hostname: {{ grains['host'] }}
        server_active: {{ server_active }}
    - require:
      - cmd: install_zabbix

up_server_scripts:
  file.managed:
    - name: /etc/init.d/zabbix_agentd
    - source: salt://zabbix/files/init.d/fedora/core/zabbix_agentd
    - template: jinja
    - defaults:
        zabbix_dir: {{ zabbix_dir }}

chkconfig_zabbix:
  cmd.run: 
    - name: chkconfig --add zabbix_agentd
    - require:
      - file: up_server_scripts
    - unless: chkconfig --list zabbix_agentd

start_zabbix:
  cmd.run:
    - name: service zabbix_agentd restart
    - unless: lsof -i:10050 


