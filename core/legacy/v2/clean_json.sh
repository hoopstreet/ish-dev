#!/bin/sh
tr -d '\n' \
| sed 's/```json//g' \
| sed 's/```//g' \
| sed 's/^[^{]*{//' \
| sed 's/}[^}]*$/}/'
