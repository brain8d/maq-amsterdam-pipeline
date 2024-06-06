## put Info here
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: "root"
      POSTGRES_PASSWORD: "root"
      POSTGRES_DB: maq_weather
    volumes:
      - $(pwd)/data:/var/lib/postgresql/maq-data
    restart: always
## Network

docker network create maq-network

# DB
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="maq_weather" \
  -v $(pwd)/data:/var/lib/postgresql/maq-data \
  -p 5432:5432 \
  --network=maq-network \
  --name maq-database \
  postgres:13

# PG ADmin
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=maq-network \
  --name pgadmin \
  dpage/pgadmin4

## aiflow services setup
## put Info here
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: "root"
      POSTGRES_PASSWORD: "root"
      POSTGRES_DB: maq_weather
    volumes:
      - $(pwd)/data:/var/lib/postgresql/maq-data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 5s
      retries: 5
    restart: always

# sql connection
create_engine('postgresql://root:root@localhost:5432/ny_taxi')

docker pull dpage/pgadmin4


# Python ingest script
python ingest_data.py \
--user=root \
--password=root \
--host=localhost \
--port=5432 \
--db=maq_weather \
--table_name=Amsterdam_april \
--data=data/Amsterdam.csv

docker build -t weather_ingest:v001 .

docker run weather_ingest:v001 \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=maq_weather \
  --table_name=Amsterdam_april \
  --data=data/Amsterdam.csv \



### Set up ssh access config file in .ssh
Host de-pipeline
    HostName 13.53.162.219
    User ubuntu
    IdentityFile ~/.ssh/aws

# running docker without sudo
https://github.com/sindresorhus/guides/blob/main/docker-without-sudo.md

# -----------


# to connect to database from VM instance in gcloud you need to:
- setup DB
- create user
- configure compute engine service (gives access to resource to the user), the VM needs to be configured with this service
- create VM instance and access with SSH
- setup according (install python, git etc)
- for the app example below install dependencies and clone repo etc.
- setup env variabes (see below)
- setup port forwarding to access on localhost


see for more: https://cloud.google.com/sql/docs/postgres/connect-instance-compute-engine#python_3
TIP: This can be automated with Terraform, the setup up of both instances with config files, saves lots of time clicking 


# Connecting to GCP DB from VM
export INSTANCE_CONNECTION_NAME='empyrean-pixel-422712-m3:europe-west4:maq-pipeline'
export DB_PORT='5432'
export DB_NAME='postgres'
export DB_USER='quickstart-user'
export DB_PASS='postgres'


# port forwarding
gcloud compute ssh maq-zoomcamp --project=empyrean-pixel-422712-m3 --zone=europe-west1-d --ssh-flag='-L 8000:127.0.0.1:8080'