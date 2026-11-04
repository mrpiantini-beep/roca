#!/bin/sh
# Arranca la sincronización de Instagram: una vez al iniciar y luego cada hora.
mkdir -p /data/ig
[ -f /data/ig/ig.json ] || echo '[]' > /data/ig/ig.json
echo "7 * * * * /usr/local/bin/ig-sync.sh >> /proc/1/fd/1 2>&1" > /etc/crontabs/root
(/usr/local/bin/ig-sync.sh || true) &
crond -b -l 8
