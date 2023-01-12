#docker cp create-user-with-pass.js  sharelatex:/var/www/sharelatex/web/modules/server-ce-scripts/scripts
## user creation isn't idempotent
#docker exec --workdir /var/www/sharelatex/web/modules/server-ce-scripts/scripts -i sharelatex node create-user-with-pass.js --email=joe1@inria.fr --pass=TestTest42
#docker exec --workdir /var/www/sharelatex/web/modules/server-ce-scripts/scripts -i sharelatex node create-user-with-pass.js --email=joe2@inria.fr --pass=TestTest42
#docker exec --workdir /var/www/sharelatex/web/modules/server-ce-scripts/scripts -i sharelatex node create-user-with-pass.js --email=joe3@inria.fr --pass=TestTest42
export CI_BASE_URL=http://localhost:8080
export CI_USERNAMES=joe1@inria.fr,joe2@inria.fr,joe3@inria.fr
export CI_PASSWORDS=TestTest42,TestTest42,TestTest42
export CI_AUTH_TYPE=community
pytest ./test_cli.py
