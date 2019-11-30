#!/usr/bin/env bash

VERSION=$(sed -n "s/__version__ = ['\"]\([^'\"]*\)['\"]/\1/p" bout_install/__init__.py)_$(date +%Y%m%d)
docker build -f docker/Dockerfile -t loeiten/bout_dev:"$VERSION" .
# NOTE: It appears that DOCKER_PASSWORD and DOCKER_USERNAME cannot be
#       set as an travis environment variable. Instead it can be set by
#       travis env set DOCKER_USERNAME myusername
#       travis env set DOCKER_PASSWORD mypassword
#       See
#       https://docs.travis-ci.com/user/docker/#building-a-docker-image-from-a-dockerfile
#       for details
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
docker push loeiten/bout_dev:"$VERSION"
docker tag loeiten/bout_dev:"$VERSION" loeiten/bout_dev:latest
docker push loeiten/bout_dev:latest