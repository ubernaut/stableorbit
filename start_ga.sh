
#!/bin/bash
echo -n "how many  python threads do you wish to start: "
read  MYTHREADS
echo  $MYTHREADS
echo -n "How many sysems would you like me to find? "
read  MYSYSTEMS
echo  $MYSYSTEMS
#xterm top &

for ((j=0;j<=MYSYSTEMS;j+=(MYTHREADS +1))); do
echo 'contents of data:'
echo | ls data
for ((i=j;i<(j+MYTHREADS);i+=1)); do
echo 'starting: '$j 'x' $i
python GA.py $i&
sleep 1
done
(j+=1)
echo 'synching on: ' $j 'x'
python GA.py $j
done



