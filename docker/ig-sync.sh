#!/bin/sh
# Sincroniza las últimas publicaciones de Instagram en /data/ig (ig.json + imágenes).
# Requiere la variable IG_TOKEN (token de larga duración de la API de Instagram).
set -eu
DATA=${IG_DATA_ROOT:-/data}/ig
LIMIT=${IG_LIMIT:-12}
TOKEN_FILE=${IG_DATA_ROOT:-/data}/ig_token
API=${IG_API:-https://graph.instagram.com}
mkdir -p "$DATA"

[ -s "$TOKEN_FILE" ] || { [ -n "${IG_TOKEN:-}" ] && printf %s "$IG_TOKEN" > "$TOKEN_FILE"; }
[ -s "$TOKEN_FILE" ] || { echo "[ig-sync] sin IG_TOKEN, se omite"; exit 0; }
TOKEN=$(cat "$TOKEN_FILE")

# Renovar el token (dura 60 días) como máximo una vez al día
if [ -z "$(find "$TOKEN_FILE" -mtime -1 2>/dev/null)" ] || [ ! -f "$DATA/.renovado" ]; then
  NEW=$(curl -fsS "$API/refresh_access_token?grant_type=ig_refresh_token&access_token=$TOKEN" | jq -r '.access_token // empty' || true)
  if [ -n "$NEW" ]; then printf %s "$NEW" > "$TOKEN_FILE"; TOKEN=$NEW; touch "$DATA/.renovado"; echo "[ig-sync] token renovado"; fi
fi

TMP=$(mktemp)
curl -fsS "$API/me/media?fields=id,caption,media_type,media_url,thumbnail_url,permalink,timestamp&limit=$LIMIT&access_token=$TOKEN" > "$TMP" \
  || { echo "[ig-sync] error al consultar Instagram"; rm -f "$TMP"; exit 1; }

KEEP=" "
jq -r '.data[] | [.id, (if .media_type=="VIDEO" then (.thumbnail_url // "") else (.media_url // "") end)] | @tsv' "$TMP" > "$TMP.list"
while IFS="$(printf '\t')" read -r id src; do
  [ -n "$src" ] || continue
  f="$id.jpg"
  if [ ! -s "$DATA/$f" ]; then
    if curl -fsS "$src" -o "$DATA/$f.tmp"; then mv "$DATA/$f.tmp" "$DATA/$f"; else rm -f "$DATA/$f.tmp"; fi
  fi
  [ -s "$DATA/$f" ] && KEEP="$KEEP$f "
done < "$TMP.list"

OUT=$(jq -c --arg keep "$KEEP" '[.data[]
  | . as $p | select($keep | contains(" " + $p.id + ".jpg "))
  | {url: .permalink, img: ("ig/" + .id + ".jpg"), video: (.media_type == "VIDEO"), fecha: .timestamp,
     alt: ((.caption // "") | gsub("\\s+"; " ") | .[0:140])}]' "$TMP")
rm -f "$TMP" "$TMP.list"

printf "%s\n" "$OUT" > "$DATA/ig.json.tmp" && mv "$DATA/ig.json.tmp" "$DATA/ig.json"
# Borrar imágenes que ya no están en el feed
for old in "$DATA"/*.jpg; do [ -e "$old" ] || continue; case "$KEEP" in *" $(basename "$old") "*) ;; *) rm -f "$old";; esac; done
echo "[ig-sync] $(jq length "$DATA/ig.json") publicaciones"
