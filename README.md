# ecom-inventory-stock-checker
Ecommerce inventory checker. We have to beat scalpers and other bots somehow.  
This script is ran everyday, every hour on the dot.

## Available ecomms:
https://www.gundamhobby.ca  
https://www.metrohobbies.ca  
https://niigs.ca  
https://scifianime.ca  

Setting up venv:
```console
python3 -m venv $VENV_NAME
```

Dependencies freeze and install:
```console
pip freeze > requirements.txt
pip install -r requirements.txt
```

How to start program:
```console
python -m cmd.main
```

## How to setup:

Pre-requisites: Docker, (Optionally) Python

1. Use `build_image.sh`
2. Setup `.env` and `postgres.env` according to the template files.
3. Use docker compose with `docker-compose.yml` to get a database running.
4. Use the `alembic` cli to setup the database migrations. (Spin up a temporary container if python is not installed)
5. Set a crontab that will run `run_gundamhobby.sh