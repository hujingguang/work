#!/bin/bash
#the scripts to used count R/s and W/s on device.and accept two Args
#arg1 is device name .etc: sda1 sda; arg2 is Read or Write , etc:R/s ,W/s

DevName=''

getDevName(){
    DevName=`mount -l|egrep '^/dev/'|egrep "$1"|cut -d' ' -f1|awk -F'/' '{print $3}'`
}


getRead(){
   r_rate=$(/usr/bin/iostat -x -m -d $1|egrep "$1" |awk '{print $6}')
   printf $r_rate
}
getWrite(){
    w_rate=$(/usr/bin/iostat -x -m -d $1|egrep "$1"|awk '{print $7}')
    printf $w_rate
}

main(){
   case $2 in
       "r/s")
          getDevName $1
          getRead $DevName
          ;;
       "w/s")
          getDevName $1
          getWrite $DevName
          ;;
      esac
}
main $1 $2






