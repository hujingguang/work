#!/bin/bash

# log login status script

HISTSIZE=10000
HISTTIMEFORMAT="%F %T "
User=$(whoami)
w|egrep "^$User" >/tmp/.info_$User
hour=$(date +"%H:%M")
Login_IP=$(grep $hour /tmp/.info_$User |awk '{print $3}')
DATE=$(date +"%y-%m-%d")
if [ ! -d /var/.history ]
then
         mkdir /var/.history
              chmod 777 /var/.history
fi
if [ ! -d /var/.history/$User ]
then
     mkdir /var/.history/$User
fi

File=/var/.history/${User}/${DATE}-${User}-${Login_IP}
if [ ! -f  ${File} ]
then
    touch $File
    chattr +a $File
fi
HISTFILE=$File

unset Login_IP File hour User

