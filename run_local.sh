#!/bin/bash
docker run --rm -it --name "run_ecom_check" -w /src -v $(pwd):/src --env-file=.env --network=host ecom-inventory-stock-checker:golang