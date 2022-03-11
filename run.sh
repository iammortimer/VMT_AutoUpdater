#! /bin/bash
DIRNAME=`dirname "$0"`

cd $DIRNAME

docker-compose run --rm vmt-autoupdater