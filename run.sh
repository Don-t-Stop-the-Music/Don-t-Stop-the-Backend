#!/bin/sh

hciconfig hci0 piscan 
hciconfig hci0 sspmode 1

cd /usr/local/dont-stop-the-music
python3 ./main.py