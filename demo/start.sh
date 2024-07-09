#!/bin/sh
/usr/sbin/sshd &
su admin -c "python3 /home/admin/app.py" &
su dave -c "node /app/app.js"