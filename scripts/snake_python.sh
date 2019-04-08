#!/bin/sh
rundir=`pwd`
echo ${rundir}
cd ..
./server.py > /dev/null 2>&1 &
./client.py -c greedy > /dev/null 2>&1 &
./client.py -c greedy > /dev/null 2>&1 &
./client.py -c greedy > /dev/null 2>&1 &
./client.py > /dev/null 2>&1 &
./monitor.py > /dev/null 2>&1 &
cd ${rundir}

