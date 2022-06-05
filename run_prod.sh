#!/bin/bash
docker run --rm -d --name "ecom-inventory-stock-checker" -w /src -v $(pwd):/src --env-file postgres.env --network=host ecom-inventory-stock-checker:ts-prod