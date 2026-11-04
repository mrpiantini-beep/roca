#!/bin/sh
# Convierte un export de Claude (bundle .html) en el sitio estático del repo.
# Uso: sh tools/build.sh /ruta/al/export.html
set -eu
SRC=$1; ROOT=$(cd "$(dirname "$0")/.." && pwd); TMP=$(mktemp -d)
cp "$SRC" "$TMP/bundle.html"
python3 -I "$ROOT/tools/1_patch_movil.py" "$TMP/bundle.html"
mkdir "$TMP/site" && python3 -I "$ROOT/tools/2_unbundle.py" "$TMP/bundle.html" "$TMP/site"
python3 -I "$ROOT/tools/3_patch_perfil.py" "$TMP/site"
python3 -I "$ROOT/tools/4_patch_instagram.py" "$TMP/site"
cp "$ROOT/assets/grain.svg" "$TMP/site/assets/grain.svg"
rm -rf "$ROOT/assets" && cp -r "$TMP/site/assets" "$ROOT/assets" && cp "$TMP/site/index.html" "$ROOT/index.html"
rm -rf "$TMP"; echo "Sitio actualizado. Revisar y hacer commit."
