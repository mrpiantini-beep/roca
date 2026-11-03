# Sitio web ROCA

Sitio estático servido con nginx. Dominio: `roca.piantinihost.com`.

- `index.html`: página (plantilla + runtime, renderiza en el navegador).
- `assets/`: scripts, fuentes e imágenes extraídos del export de Claude.

## Despliegue en Dokploy
- Build Type: `Dockerfile`, Docker File: `Dockerfile`, Context: `.`
- Puerto del contenedor: `80`

## Prueba local
```bash
docker build -t roca . && docker run --rm -p 8080:80 roca
```
