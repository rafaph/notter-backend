#!/bin/sh

# Adds the citext extension to database and test database
"${psql[@]}" <<- 'EOSQL'
CREATE EXTENSION IF NOT EXISTS citext;
\c template1
CREATE EXTENSION IF NOT EXISTS citext;
EOSQL
