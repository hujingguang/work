{% set server_ip = '192.168.16.243' %}
up_conf:
  file.managed:
    - name: /soft/zabbix/etc/zabbix_agentd.conf
    - source: salt://zabbix/files/zabbix_agentd.conf
    - template: jinja
    - user: zabbix
    - group: zabbix
    - defaults:
        Server: {{ server_ip }}
        ServerActive: {{ server_ip }}
        host: {{ grains['ip4_interfaces']['eth0'][0] }}
