add_zbx_user:
  user.present:
    - name: zabbix
    - shell: /sbin/nologin
    - createhome: False
    - gid_from_name: True
    - system: True
        
