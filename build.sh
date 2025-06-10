#!/bin/bash

base=$( realpath $(dirname $0) )
image=srh-playwright

echo "🐳 docker build"
docker build -t $image $base
