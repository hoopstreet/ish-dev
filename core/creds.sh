#!/bin/sh

mkdir -p /root/.creds
FILE="/root/.creds/data.txt"

echo "1 Add"
echo "2 Get"
read c

case $c in
1) read -p "Key: " k; read -p "Value: " v; echo "$k=$v" >> $FILE ;;
2) cat $FILE ;;
esac
