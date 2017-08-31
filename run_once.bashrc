#!/bin/bash -e
if [ ! -d /Users/mswanholm/self-service ]; then
  mkdir -p /Users/mswanholm/self-service;
fi

DEMODIR=`/Users/mswanholm/self-service $0`/..

#ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

#export PATH=/usr/local/bin:/usr/local/sbin:$PATH

#brew install python3

cd $DEMODIR/..

pip install -e git+git://github.com/gotransverse/self-service.git
