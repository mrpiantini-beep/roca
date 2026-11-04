# Sitio web ROCA

Sitio estático servido con nginx. Dominio: `roca.piantinihost.com`.

- `index.html`: página (plantilla + runtime, renderiza en el navegador).
- `assets/`: scripts, fuentes e imágenes extraídos del export de Claude.
- `docker/`: sincronización de Instagram (cron dentro del contenedor).
- `tools/`: scripts para convertir un export nuevo de Claude (`sh tools/build.sh export.html`).

## Despliegue en Dokploy
- Build Type: `Dockerfile`, Docker File: `Dockerfile`, Context: `.`
- Puerto del contenedor: `80`
- Variable de entorno: `IG_TOKEN` = token de larga duración de la API de Instagram.
- Volumen: montar un volumen en `/data` (guarda el token renovado y las imágenes).

## Instagram
`docker/ig-sync.sh` corre al iniciar y cada hora (minuto 7):
1. Renueva el token una vez al día (dura 60 días; renovándolo no caduca).
2. Descarga las últimas 12 publicaciones a `/data/ig` y genera `ig.json`.
3. La página lee `/ig/ig.json`. Sin token o sin datos, muestra "Síganos en Instagram".

Forzar una sincronización: `docker exec <contenedor> ig-sync.sh`

## Prueba local
```bash
docker build -t roca . && docker run --rm -p 8080:80 -e IG_TOKEN=xxx -v roca-data:/data roca
```
