up_scripts_dir:
  file.recurse:
    - name: /soft/zabbix/share/zabbix/alertscripts/scripts
    - source: salt://zabbix/files/scripts
    - user: zabbix
    - group: zabbix
    - dir_mode: 755
    - file_mode: 755
    - include_empty: True
