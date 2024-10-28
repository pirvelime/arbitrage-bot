#!/bin/bash
#
#
./.venv/bin/python main.py

rm /tmp/opportunities.txt

echo 'Running formatter to display opportunities nicely...'
grep '%' opportunities/* |
  while read o
  do
    x="${o##*on }"
    echo "$x" | sed 's/\(.*\): \(.*\)/\2 \1/'  >> /tmp/opportunities.txt
  done
sort /tmp/opportunities.txt
