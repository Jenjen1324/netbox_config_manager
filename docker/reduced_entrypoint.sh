#!/bin/bash
# Modified version of: https://github.com/netbox-community/netbox-docker/blob/release/docker/docker-entrypoint.sh
# Runs on every start of the NetBox Docker container

# Stop when an error occures
set -e

# Allows NetBox to be run as non-root users
umask 002

# Load correct Python3 env
# shellcheck disable=SC1091
source /opt/netbox/venv/bin/activate

# Try to connect to the DB
DB_WAIT_TIMEOUT=${DB_WAIT_TIMEOUT-3}
MAX_DB_WAIT_TIME=${MAX_DB_WAIT_TIME-30}
CUR_DB_WAIT_TIME=0
while [ "${CUR_DB_WAIT_TIME}" -lt "${MAX_DB_WAIT_TIME}" ]; do
  # Read and truncate connection error tracebacks to last line by default
  pg_isready -h $DB_HOST -U $DB_USER && break
  echo "⏳ Waiting on DB... (${CUR_DB_WAIT_TIME}s / ${MAX_DB_WAIT_TIME}s)"
  sleep "${DB_WAIT_TIMEOUT}"
  CUR_DB_WAIT_TIME=$((CUR_DB_WAIT_TIME + DB_WAIT_TIMEOUT))
done
if [ "${CUR_DB_WAIT_TIME}" -ge "${MAX_DB_WAIT_TIME}" ]; then
  echo "❌ Waited ${MAX_DB_WAIT_TIME}s or more for the DB to become ready."
  exit 1
fi

# Launch whatever is passed by docker
# (i.e. the RUN instruction in the Dockerfile)
exec "$@"