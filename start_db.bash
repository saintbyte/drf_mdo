#!/bin/bash
set -x
docker run --name ripe-pg-15\
          --rm\
          -p 5432:5432\
          -e POSTGRES_USER=postgres\
          -e POSTGRES_PASSWORD=change111\
          -e POSTGRES_DB=mdo\
          -e PGDATA="/var/lib/postgresql/data/pgdata"\
          -v /home/sb/tests/mdo/db:/var/lib/postgresql/data\
           postgres
