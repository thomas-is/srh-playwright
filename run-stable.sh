#!/bin/bash

base=$( realpath $(dirname $0) )
image=srh-playwright

echo "🚀 docker run"
docker run --rm -it \
  --name $image \
  --env-file $base/env \
  -v $base/videos:/home/python/videos \
  $image
