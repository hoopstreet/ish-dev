#!/bin/sh

echo "=== PROJECT MANAGER ==="
echo "1. Create project"
echo "2. Enter project"
echo "3. List projects"
echo "0. Back"

read c

case $c in
1)
  echo "Project name:"
  read name
  mkdir -p /root/projects/$name
  echo "Created: $name"
;;
2)
  echo "Enter project name:"
  read name
  cd /root/projects/$name || echo "Not found"
  sh
;;
3)
  ls /root/projects
;;
esac
