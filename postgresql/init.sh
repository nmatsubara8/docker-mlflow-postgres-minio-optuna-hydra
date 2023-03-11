#!/bin/bash
set -e

psql -v ON_ERROR_STOP=1 --username "$DB_USER" <<-EOSQL
    CREATE DATABASE ${DB_NAME};
EOSQL