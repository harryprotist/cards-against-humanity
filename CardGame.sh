#!/bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
python2 $DIR/resources/CardGame.py $1 $2 $3
