#!/bin/bash
docker run -w /src -v $(pwd):/src --network=host ecom-inventory-stock-checker:latest bash -c "python3 -m cmd.gundamhobby"