#!/bin/bash

set -e

echo $MONGO_REPLICA_SET_KEY > /data/configdb/keyFile
chmod 400 /data/configdb/keyFile
chown mongodb:mongodb /data/configdb/keyFile
