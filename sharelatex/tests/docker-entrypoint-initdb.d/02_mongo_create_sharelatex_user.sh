
#!/bin/bash

set -e

mongosh -u $MONGO_INITDB_ROOT_USERNAME -p $MONGO_INITDB_ROOT_PASSWORD <<EOF
use sharelatex
db.createUser({
  user:  '$MONGO_OVERLEAF_USER',
  pwd: '$MONGO_OVERLEAF_PASSWORD',
  roles: [{
    role: 'readWrite',
    db: 'sharelatex'
  }]
})
EOF

# in js
# db = db.getSiblingDB("sharelatex");
# db.createUser({user: process.env["MONGO_OVERLEAF_USER"], pwd: process.env["MONGO_OVERLEAF_PASSWORD"], roles: [{role: "readWrite", db: "sharelatex"}]});
