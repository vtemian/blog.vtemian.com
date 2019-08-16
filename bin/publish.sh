#!/bin/bash

set -x

credentials.sh

cp -R public resources /tmp/

git stash
git log -1 --pretty=%B > /tmp/msg
git checkout master

ls | egrep -v '.git|CNAME' | xargs rm -r
cp -R /tmp/public/* .
#cp -R /tmp/resources/_gen/assets/css/output/* output/
#cp -R /tmp/resources/_gen/assets/js/output/* output/

git add .
git commit -m "Published: $(cat /tmp/msg)"
git push origin master
