#!/usr/bin/env sh
cd database/postgres || mkdir "database/postgres"
docker-compose up --build -d
