#!/bin/bash

CURRENTTIME=$(date +"%Y-%m-%d-%H-%M")
NAME=$1

FILENAME="$CURRENTTIME"-"$NAME".md

printf "# $CURRENTTIME $NAME\n\n\n" > $FILENAME
printf "## Links\n" >> $FILENAME

MD_EDITOR=$(cat .editor)

if [ -z "$MD_EDITOR" ]
then
	MD_EDITOR=$EDITOR
fi

$MD_EDITOR $FILENAME

git add $FILENAME
git commit -m "Add note about ${NAME}"
git push

python converter.py
