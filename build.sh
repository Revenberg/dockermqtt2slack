#!/bin/bash

# version 2021-08-07 15:20

cd ~/dockermqtt2slack

if [ -n "$1" ]; then
  ex=$1
else
  rc=$(git remote show origin |  grep "local out of date" | wc -l)
  if [ $rc -ne "0" ]; then
    ex=true
  else
    ex=false
  fi
fi

if [ $ex == true ]; then
    git pull
    chmod +x build.sh

    docker image build -t revenberg/mqtt2slack .

    docker push revenberg/mqtt2slack

    # testing: 

    echo "==========================================================="
    echo "=                                                         ="
    echo "=          docker run revenberg/mqtt2slack                ="
    echo "=                                                         ="
    echo "==========================================================="
    # docker run revenberg/mqtt2slack
fi

cd -
