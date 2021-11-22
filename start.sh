#!/bin/sh

if [ -f .env ]; then
    echo "Loading environment variables"
    export $(cat .env | xargs)
else
    echo "No environment file found, please run with --prepare option"
fi

if  [[ $1 = "--restart-all" ]]; then
    echo "Restarting domoticz service"
    sudo service domoticz restart
    echo "Restarting bluetooth service"
    sudo systemctl stop hciuart.service
    sudo systemctl start hciuart.service
fi

exit