#!/bin/sh
service ssh start &
su mysql -c "docker-entrypoint.sh mysqld"