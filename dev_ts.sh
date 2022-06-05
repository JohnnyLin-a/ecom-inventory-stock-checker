#!/bin/bash
docker run --rm -it -v $PWD:/src -w /src --env-file postgres.env node:18-alpine sh