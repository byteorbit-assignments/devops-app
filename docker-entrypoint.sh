#!/usr/bin/env bash

# Wait for services we depend on (db, cache, etc)
read -ra WAIT_FOR_ADDR <<< ${WAIT_FOR}
for addr in "${WAIT_FOR_ADDR[@]}"; do
    wait-for-it -t 60 ${addr}
done

# run CMD
exec "$@"
