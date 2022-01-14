#!/bin/bash

help_me () {
    echo "-h --help : Display this message"
    echo "-i --install : Install necessary packages"
    echo "no argument : Start automations"
}

install () {
    sudo apt-get update -y
    sudo apt-get upgrade -y
    sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget python3 pip3 -y
    # export PATH=$PATH:/usr/bin
    pip3 install PyP100 lywsd03mmc
}

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -i|--install) install; shift ;;
        -h|--help) help_me ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    exit 1
done

set_environment () {
    if [ -f .env ]
    then
        export $(cat .env | xargs)
    fi
}

run_automations () {
    nohup python3 -u /home/pi/domoticz/scripts/customs/main.py > /home/pi/domoticz/scripts/customs/automations.log &
}

set_environment
run_automations