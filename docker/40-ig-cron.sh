#!/bin/sh
# Arranca la sincronización de Instagram: una vez al iniciar y luego cada hora.
mkdir -p /data/ig
[ -f /data/ig/ig.json ] || echo '[]' > /data/ig/ig.json
# Behold gratis actualiza cada 24 h: consultar cada 3 h (~240 visitas/mes de 1.200)
if [ -n "${BEHOLD_FEED_URL:-}" ]; then SCHED="7 */3 * * *"; else SCHED="7 * * * *"; fi
echo "$SCHED /usr/local/bin/ig-sync.sh >> /proc/1/fd/1 2>&1" > /etc/crontabs/root
(/usr/local/bin/ig-sync.sh || true) &
crond -b -l 8
