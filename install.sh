#!/bin/sh

if  [[ $1 = "--prepare" ]]; then
    echo "Copying environment file"
    cp .env.example .env
    crontab -l > tmpcron
    echo "@reboot $(pwd)/start.sh" >> tmpcron
    crontab tmpcron
    rm tmpcron
    
    echo "Edit .env file with custom values and re-run this script with --start option"
    exit
fi

sudo apt-get update
sudo apt -y upgrade
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev python3-pip
pip3 install pyyaml requests Adafruit_DHT lywsd03mmc