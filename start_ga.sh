#!/bin/bash
for ((i=0;i<=8;i+=1)); do
echo 'starting: '$i
python GA.py $i&
sleep 1

done

