{% set base_dir = '/soft/mysql' %}
{% set data_dir = '/data/mysql' %}
{% set mysql_user = 'mysql' %}
{% set mysql_group = 'mysql' %}

uptar:
  file.managed:
    - name: /tmp/mysql-5.6.10.tar.gz
    - mode: 777
    - source: salt://mysql/files/mysql-5.6.10.tar.gz

adduser:
  user.present:
    - name: mysql
    - gid_from_name: True
    - shell: /sbin/nologin
    - createhome: False
    - system: True


unpack:
  cmd.run:
    - cwd: /tmp
    - name: tar -xvzf mysql-5.6.10.tar.gz
    - require:
      - file: uptar
    - unless: test -d /tmp/mysql

cmake:
  pkg.installed:
    - pkgs:
      - cmake
      - ncurses-devel
      - gcc
      - gcc-c++
      - libgcc



configure:
  cmd.run:
    - name: cd /tmp/mysql-5.6.10 && cmake -DCMAKE_INSTALL_PREFIX={{ base_dir }} -DMYSQL_DATADIR={{ data_dir }} -DSYSCONFIGDIR={{ base_dir }} -DWITH_INNOBASE_STORAGE_ENGINE=1 -DWITH_MEMORY_STORAGE_ENGINE=1 -DWITH_MYISAM_STORAGE_ENGINE=1 -DWITH_ARCHIVE_STORAGE_ENGINE=1 -DWITH_READLINE=1 -DENABLED_LOCAL_INFILE=1 -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci -DEXTRA_CHARSET=utf8 -DWITH_USER={{ mysql_user }} && make && make install
    - require:
      - pkg: cmake
      - cmd: unpack
    - unless: test -d /soft/mysql 

up_myconf:
  file.managed:
    - name: {{ base_dir }}/my.cnf
    - source: salt://mysql/files/my.cnf
    - mode: 666
    - user: {{ mysql_user }}
    - template: jinjia
    - defaults:
      base_dir: {{ base_dir }}
      data_dir: {{ data_dir }}
    - require:
      - cmd: configure



up_server_scripts:
  file.managed:
    - name: /soft/mysql/mysql.server
    - source: salt://mysql/files/mysql.server.sh
    - mode: 555
    - template: jinja
    - defaults:
      base_dir: {{ base_dir }}
      data_dir: {{ data_dir }}

chmodfile:
  cmd.run:
    - name: chown -R {{ mysql_user }}.{{ mysql_group }} {{ data_dir }} && chown -R {{ mysql_user }}.{{ mysql_group }} {{ base_dir }}
    - require:
      - cmd: configure
    - unless: test -d {{ data_dir }}



init_database:
  cmd.run:
    - name: /soft/mysql/scripts/mysql_install_db  --datadir={{ data_dir }} --basedir={{ base_dir }} --user=mysql
    - require:
      - cmd: configure
    - unless: test -d {{ data_dir }}/mysql

start_mysqlserver:
  cmd.run:
    - name: {{ base_dir }}/mysql.server restart
    - watch:
      - cmd: init_database
      - file: up_myconf

