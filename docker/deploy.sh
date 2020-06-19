#!/usr/bin/env bash

printf "\nObtaining version\n"
VERSION=$(sed -n "s/__version__ = ['\"]\([^'\"]*\)['\"]/\1/p" bout_install/__init__.py)_$(date +%Y%m%d)
IMAGE=loeiten/bout_dev
printf '\nCurrent version %s\n' "$VERSION"
printf "\nBuilding image\n"
docker build -f docker/Dockerfile -t "$IMAGE":"$VERSION" .
printf "\nTesting build\n"
# Test that the build is working
# NOTE: The /bin/sh is already stated in the ENTRYPOINT
docker run --rm -it "$IMAGE":"$VERSION" -c 'cd $HOME/BOUT-dev/examples/conduction && make && ./conduction'
printf "\nTest Passed\n"
# NOTE: DOCKER_PASSWORD and DOCKER_USERNAME are environment secrets of
#       the github repo
echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin
printf '\nPushing %s\n' "$IMAGE:$VERSION"
docker push "$IMAGE":"$VERSION"
docker tag "$IMAGE":"$VERSION" "$IMAGE":latest
printf '\nPushing %s\n' "$IMAGE:$VERSION"
docker push "$IMAGE":latest
printf "\nSuccess\n"