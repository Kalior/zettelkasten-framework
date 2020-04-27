#! /bin/bash
FIND=$1
NAME=$(basename $1 .md)

rg --context 10 -e "$NAME" *.md
