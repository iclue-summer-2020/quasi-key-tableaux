#!/usr/bin/env bash
set -e
docker build -t icluesu2020/qkt-server:latest .
docker run --rm -p 5000:5000 -it icluesu2020/qkt-server:latest
