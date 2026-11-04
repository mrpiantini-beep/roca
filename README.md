# Sitio web ROCA

Sitio estático servido con nginx. Dominio: `roca.piantinihost.com`.

- `index.html`: página (plantilla + runtime, renderiza en el navegador).
- `assets/`: scripts, fuentes e imágenes extraídos del export de Claude.
- `docker/`: sincronización de Instagram (cron dentro del contenedor).
- `tools/`: scripts para convertir un export nuevo de Claude (`sh tools/build.sh export.html`).

## Despliegue en Dokploy
- Build Type: `Dockerfile`, Docker File: `Dockerfile`, Context: `.`
- Puerto del contenedor: `80`
- Variable de entorno (una de las dos):
  - `BEHOLD_FEED_URL` = URL del feed JSON de behold.so (plan gratis, 6 publicaciones). **Opción actual.**
  - `IG_TOKEN` = token de larga duración de la API oficial de Instagram (hasta 12 publicaciones).
- Volumen: montar un volumen en `/data` (guarda las imágenes y el token renovado).

## Instagram
`docker/ig-sync.sh` corre al iniciar y luego por cron:
- **Behold** (`BEHOLD_FEED_URL`): cada 3 horas (~240 consultas/mes de las 1.200 gratis; Behold gratis actualiza cada 24 h).
- **API oficial** (`IG_TOKEN`): cada hora; renueva el token una vez al día.

Descarga las imágenes a `/data/ig` y genera `ig.json`; la página lee `/ig/ig.json`.
Si la fuente falla o llega vacía, se conservan los datos anteriores.
Sin configuración o sin datos, la página muestra "Síganos en Instagram".

Forzar una sincronización: `docker exec <contenedor> ig-sync.sh`

## Prueba local
```bash
docker build -t roca . && docker run --rm -p 8080:80 -e BEHOLD_FEED_URL=https://feeds.behold.so/XXXX -v roca-data:/data roca
```
