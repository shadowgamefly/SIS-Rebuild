#!/bin/bash

sleep 40

if [[ -e /app/db/cs4501 ]] ; then
    mysql -uroot -p'$3cureUS' -h db -Bse \
    "drop database cs4501;
    create database cs4501 character set utf8;
    grant all on *.* to 'www'@'%'; \
    ";
else
    mysql -uroot -p'$3cureUS' -h db -Bse \
    "create user 'www'@'%' identified by '\$3cureUS';
    create database cs4501 character set utf8;
    grant all on *.* to 'www'@'%'; \
    ";
fi

echo "Success!"
