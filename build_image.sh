#!/bin/bash
docker buildx build --pull -t ecom-inventory-stock-checker:latest -f Dockerfile .