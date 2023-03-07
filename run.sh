#!/bin/sh

sleep 10

hciconfig hci0 piscan 
hciconfig hci0 sspmode 1

python3 ./main.py