include:
  - zabbix.add_zbx_user
  - zabbix.install_zbx_agent
  - zabbix.update_zbx_conf
  - zabbix.up_scripts

start_zbx_agentd:
  service.running:
    - name: zabbix_agentd
    - enable: True
    - watch:
      - file: /soft/zabbix/etc/zabbix_agentd.conf 
