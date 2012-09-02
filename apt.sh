#!/usr/bin/env bash







V=${1:-2.1.0}
sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 4F7B93595D50B6BA
sudo sed -re "s:mapnik/v[^/]*:mapnik/v$V:g" -i /etc/apt/sources.list
sudo apt-get update
sudo apt-get install --reinstall libmapnik-dev mapnik-utils mapnik-doc libmapnik \
g++ cpp \
  libicu-dev \
  libboost-filesystem-dev \
  libboost-program-options-dev \
  libboost-python-dev libboost-regex-dev \
  libboost-system-dev libboost-thread-dev \
  python-dev libxml2 libxml2-dev \
  libfreetype6 libfreetype6-dev \
  libjpeg-dev \
  libltdl7 libltdl-dev \
  libpng-dev \
  libproj-dev \
  libgeotiff-dev libtiff-dev libtiffxx0c2 \
  libcairo2 libcairo2-dev python-cairo python-cairo-dev \
  libcairomm-1.0-1 libcairomm-1.0-dev \
  ttf-unifont ttf-dejavu ttf-dejavu-core ttf-dejavu-extra \
  git build-essential python-nose clang \
  libgdal1-dev python-gdal \
  postgresql-9.1 postgresql-server-dev-9.1 postgresql-contrib-9.1 postgresql-9.1-postgis \
  libsqlite3-dev \
	-y --force-yes


