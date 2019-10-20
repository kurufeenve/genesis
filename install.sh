#!/bin/bash

path=$(pwd)
activate () {
  . /bin/activate
}

if command -v python3 &>/dev/null; then
    pip3 install virtualenv
    mkdir venv storage
    touch storage/server_config
    echo "127.0.0.1" > storage/server_config
    echo "5000" >> storage/server_config
    python3 -m venv $path/venv
    source "./venv/bin/activate"
    pip3 install -r requirements.txt
    pip3 install base58
    pip3 install ecdsa
    pip3 install requests
    pip3 install Flask
    pip3 install flask-restful
    echo
    echo "=========="
    echo
    echo "to run wallet_cli or miner_cli first run 'source bin/activate'
    then corresponding script"
    echo
    echo "=========="
    echo

else
    echo "Python 3 is not installed. 
    If you are on mac in school 42 install python3 throught managed software center 
    and run this script one more time"
fi
