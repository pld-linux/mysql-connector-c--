#!/bin/sh
p=mysql-connector-c++
v=1.1.0
r=916

d=$p-$v
t=$p-bzr$r.tar.xz

set -e

if [ ! -d $d ]; then
	bzr branch -r $r lp:~mysql/mysql-connector-cpp/trunk $d
else
	cd $d
	bzr pull
	bzr up -r $r
	cd ..
fi

# check getDriverMajorVersion / getDriverMinorVersion / getDriverPatchVersion
grep sql::SQLString.version.*$v $d/driver/mysql_metadata.cpp

tar -cJf $t --exclude-vcs $d
