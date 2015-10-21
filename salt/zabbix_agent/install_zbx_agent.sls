up_zbx_gz:
  file.managed:
    - name: /tmp/zabbix.tar.gz
    - source: salt://zabbix/files/zabbix.tar.gz

unzip_zbx_gz:
  cmd.run:
    - name: cd /tmp && tar -zxvf zabbix.tar.gz && mv /tmp/soft/zabbix /soft/zabbix 
    - require:
      - file: /tmp/zabbix.tar.gz
    - unless: test -d /soft/zabbix

chown_zbx_dir:
  cmd.run:
    - name: chown -R zabbix.zabbix /soft/zabbix
    - require:
      - cmd: unzip_zbx_gz
    - unless: test -d /soft/zabbix

service_script:
  file.managed:
    - name: /etc/init.d/zabbix_agentd
    - source: salt://zabbix/files/zabbix_agentd
    - mode: 755
  cmd.run:
    - name: chkconfig --add zabbix_agentd
    - unless: chkconfig --list|grep zabbix_agentd       

