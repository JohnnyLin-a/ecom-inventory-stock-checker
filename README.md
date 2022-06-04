# ecom-inventory-stock-checker
Ecommerce inventory checker. We have to beat scalpers and other bots somehow.  
This script is ran everyday, every hour on the dot.

## Available ecomms:
https://www.gundamhobby.ca  
https://www.metrohobbies.ca  
https://niigs.ca  
https://scifianime.ca  


## How to setup:

Pre-requisites: Docker

1. Use `build_image.sh`
2. Setup `.env` and `postgres.env` according to the template files.
3. Use docker compose with `docker-compose.yml` to get a database running.
4. Use the `alembic` cli to setup the database migrations. (Spin up a temporary container if python is not installed)
5. Set a crontab that will run `run_gundamhobby.sh