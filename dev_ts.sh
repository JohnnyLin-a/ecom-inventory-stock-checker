#!/bin/bash
docker run --rm -it -v $PWD:/src -w /src --env-file postgres.env --network host node:18-alpine sh