#!/usr/bin/env bash

aptitude update

yes | aptitude install git-core redis-server python3-dev python3-pip gettext libxml2-dev libxslt1-dev zlib1g-dev

pip3 install -r /vagrant/requirements.txt
