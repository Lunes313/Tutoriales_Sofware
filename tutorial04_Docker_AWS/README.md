# Tutorial 04 - Docker + AWS (Django + PostgreSQL)

Este taller deja la aplicacion Django lista para correr en contenedores y desplegar en una VM Linux (AWS EC2 o WSL).

## Objetivo

- Levantar la API con Docker Compose.
- Usar PostgreSQL en contenedor.
- Probar el endpoint de compra en entorno dockerizado.

## Requisitos

- Docker Desktop (con Docker Compose).
- PowerShell o terminal bash.

## Ejecutar local con Docker

Desde esta carpeta `tutorial04_Docker_AWS`:

```bash
docker compose up -d --build
docker compose ps
```

Si el puerto 8000 esta ocupado, ejecuta con otro puerto:

```bash
set WEB_PORT=8001
docker compose up -d --build
```

En Linux/macOS:

```bash
WEB_PORT=8001 docker compose up -d --build
```

## Migraciones y datos de prueba

```bash
docker compose exec web python manage.py migrate
docker compose exec web python manage.py shell
```

Dentro del shell de Django:

```python
from tienda_app.models import Libro, Inventario
libro = Libro.objects.create(titulo="Docker AWS", precio=120.0)
Inventario.objects.create(libro=libro, cantidad=5)
print(libro.id)
```

## Probar endpoint

```bash
curl -X POST http://127.0.0.1:8000/api/v1/comprar/ -H "Content-Type: application/json" -d "{\"usuario\":\"Laura\",\"direccion_envio\":\"Bogota\",\"productos\":[{\"libro_id\":1,\"cantidad\":1}]}"
```

Si cambiaste el puerto usa `8001` (o el que hayas definido).

## Logs utiles

```bash
docker compose logs -f web
docker compose logs -f db
```

## Apagar y limpiar contenedores

```bash
docker compose down
```

Para borrar tambien el volumen de PostgreSQL:

```bash
docker compose down -v
```
