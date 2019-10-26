#!/usr/bin/env bash

docker build -f docker/Dockerfile -t loeiten/fruit_classifier:latest .
# NOTE: It appears that DOCKER_PASSWORD and DOCKER_USERNAME cannot be
#       set as an travis environment variable. Instead it can be set by
#       travis env set DOCKER_USERNAME myusername
#       travis env set DOCKER_PASSWORD mypasswor
#       See
#       https://docs.travis-ci.com/user/docker/#building-a-docker-image-from-a-dockerfile
#       for detaills
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
VERSION=`grep -E "^__version__ = ['\"]([^'\"]*)['\"]" __init__.py | grep -oEi "\d+\.\d+\.\d+"`
docker push loeiten/fruit_classifier:$(VERSION)
