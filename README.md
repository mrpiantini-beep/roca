# Sitio web ROCA

Sitio estático (HTML autocontenido) servido con nginx. Dominio: `roca.piantinihost.com`.

## Despliegue en Dokploy
- Build Type: `Dockerfile`, Build Path: `/`
- Puerto del contenedor: `80`

## Prueba local
```bash
docker build -t roca . && docker run --rm -p 8080:80 roca
```
