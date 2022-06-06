#!/bin/bash
docker run --rm -d --name "ecom-inventory-stock-checker" -w /dist --env-file postgres.env --env-file .env --network=host ecom-inventory-stock-checker:latest