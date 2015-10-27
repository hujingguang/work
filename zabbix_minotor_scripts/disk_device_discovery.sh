#!/bin/bash

dev_array=(`iostat -x -d |egrep -v 'Device|Linux|^$' |grep -i "$1"|cut -d' ' -f1 `)
len=${#dev_array[@]}
flag=0



printf "{\t\t\n"
printf  '\t'"\"data\":["


for i in  ${dev_array[@]}
   do
      flag=$[$flag+1]
     printf '\n\t\t{'
     printf "\"{#DEV_NAME}\":\"$i\"}"
     if [ $flag -lt $len ]
       then
         printf ','
     else
         printf ''
     fi
   done


printf  "\n\t]\n"

printf "}\n"

#echo ${#dev_array[@]}
