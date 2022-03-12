#! /bin/bash
DIRNAME=`dirname "$0"`

cd $DIRNAME

docker-compose run vmt-autoupdater

# docker-compose run --rm vmt-autoupdater
