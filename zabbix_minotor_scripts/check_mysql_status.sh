#!/bin/bash

MysqlBin=/soft/mysql/bin/mysql
User='zbx_chk'
Pass='chk_zbx'

if [ $@ \< 1 ]
then
    echo  args less than 1 !
    exit
fi

$MysqlBin -u$User -p$Pass -h 127.0.0.1 -e "show global status like '$1'; " 2>/dev/null |grep -v 'Value'|awk 'NF>1 {print $2}'           

exit 
case $1 in
    "Com_begin")
        $MysqlBin -u$User -p$Pass -h 127.0.0.1 -e "show global status like '$1'; " 2>/dev/null |grep -v 'Value'|awk 'NF>1 {print $2}'           
        ;;
    "Bytes_received")
        
        ;;
    "Bytes_sent")
        
        ;;
    "Com_commit")

        ;;
    "Com_delete")

        ;;
    "Com_insert")

        ;;
    "Questions")
        
        ;;
    "Com_rollback")

        ;;
    "Com_select")

        ;;
    "Slow_queries")

        ;;
    "Com_update")

        ;;
    "Uptime")

        ;;
    esac





