#!/bin/bash

set -o errexit

readonly REQUIRED_ENV_VARS=(
    "POSTGRES_USER"
    "DATA_DB_USER"
    "DATA_DB_USER_PASSWORD"
    "DATA_DB")


main() {
  check_env_vars_set
  init_user_and_db
}


check_env_vars_set() {
  for required_env_var in ${REQUIRED_ENV_VARS[@]}; do
    if [[ -z "${!required_env_var}" ]]; then
      echo "Error:
    Environment variable '$required_env_var' not set.
    Make sure you have the following environment variables set:
      ${REQUIRED_ENV_VARS[@]}
Aborting."
      exit 1
    fi
  done
}


init_user_and_db() {
  psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" <<-EOSQL
     CREATE USER $DATA_DB_USER WITH PASSWORD '$DATA_DB_USER_PASSWORD';
     CREATE DATABASE $DATA_DB;
     GRANT ALL PRIVILEGES ON DATABASE $DATA_DB TO $DATA_DB_USER;
EOSQL
}

main "$@"