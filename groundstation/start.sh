#!/bin/bash

chmod 755 /data

chown -R security:security /data/security
chown -R research:research /data/research
chown -R helpdesk:helpdesk /data/helpdesk
chown -R hr:hr /data/hr

chmod -R 700 /data/research
chmod -R 700 /data/helpdesk
chmod -R 700 /data/security
chmod -R 700 /data/hr

chown nobody:nogroup /data/public
chmod a-w /data/public
chmod +rx /data/public

service vsftpd start

/usr/sbin/sshd -D