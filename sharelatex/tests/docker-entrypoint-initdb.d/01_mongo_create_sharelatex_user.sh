
#!/bin/bash

set -e

mongo <<EOF
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
