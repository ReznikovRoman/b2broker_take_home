#!/bin/bash

echo "** Configuring permissions for the user"

mysql -u root -p$MYSQL_ROOT_PASSWORD --execute \
"GRANT ALL ON *.* TO '${MYSQL_USER}'@'%';
FLUSH PRIVILEGES;"

echo "** Finished configuring permissions for the user"
