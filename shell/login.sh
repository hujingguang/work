#!/bin/bash

# log login status script

HISTSIZE=10000
HISTTIMEFORMAT="%F %T "
User=$(whoami)
who|tail -n 1  >/tmp/.info_$User
Login_IP=$(cat /tmp/.info_$User |awk -F'[)(]' '{print $2}')
DATE=$(date +"%y-%m-%d")
if [ ! -d "/var/.history" ]
then
             mkdir /var/.history
                           chmod 777 /var/.history
                       fi
                       if [ ! -d "/var/.history/$User" ]
                       then
                               mkdir /var/.history/$User
                           fi

                           File=/var/.history/${User}/${DATE}_${User}_${Login_IP}
                           if [ ! -e  "$File" ]
                                   then
                                           touch $File
                                               chattr +a $File
                                           fi

                                           HISTFILE=$File


                                           unset Login_IP File hour User

