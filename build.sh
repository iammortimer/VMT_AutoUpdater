#!/bin/bash

DIRNAME=`dirname "$0"`

cd $DIRNAME

docker build -t vmtautoupdater .
