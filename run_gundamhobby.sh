#!/bin/bash
docker run --rm -d --name "run_gundamhobbby" -w /src -v $(pwd):/src -e PYTHONUNBUFFERED=1 --network=host ecom-inventory-stock-checker:latest bash -c "python3 -m cmd.main"