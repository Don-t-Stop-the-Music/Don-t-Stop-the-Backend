#!/bin/sh

if [ $(whoami) != "root" ]
then
    echo "Must be run as root!"
    exit 1
else
    mkdir -p /usr/local/dont-stop-the-music
    install \
        bluetooth_process.py \
        config.py \
        feedback_hiss_analyser.py \
        freq_analyser.py \
        main.py \
        utility.py \
        /usr/local/dont-stop-the-music/
    install -m +x \
        run.sh \
        /usr/local/dont-stop-the-music/
    install \
        dont-stop-the-music.service \
        /etc/systemd/system/
    systemctl enable dont-stop-the-music
fi
    