#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
(
cd $DIR/resources;
python2 CardGame.py $1 $2 $3
) # makes sure that program doesn't exit in 'resources'
