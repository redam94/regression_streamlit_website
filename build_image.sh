#!bin/bash
docker build -t redam94/regression:$(git rev-parse --abbrev-ref HEAD| sed 's/[^a-zA-Z0-9]//g') .
docker push redam94/regression:$(git rev-parse --abbrev-ref HEAD| sed 's/[^a-zA-Z0-9]//g')


