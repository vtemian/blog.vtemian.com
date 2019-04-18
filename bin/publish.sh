#!/bin/bash

set -x

credentials.sh

cp -R public/ /tmp/

git log -1 --pretty=%B > /tmp/msg
git checkout master

ls | egrep -v '.git|CNAME' | xargs rm -r
cp -R /tmp/public/* .

git add .
git commit -m "Published: $(cat /tmp/msg)"
git push origin master
