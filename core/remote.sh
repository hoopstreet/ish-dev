#!/bin/sh

echo "1. List Projects"
echo "2. Add Project"
read c

case $c in
1) ls /root/projects ;;
2) read -p "Git URL: " url; git clone $url /root/projects ;;
esac
