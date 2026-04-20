# Tutorial 05 - Nginx + Gunicorn (Base del Strangler Pattern)

Este tutorial reemplaza el servidor de desarrollo de Django por Gunicorn y pone Nginx
al frente como proxy inverso. Django queda aislado en la red interna de Docker y solo
Nginx expone el servicio al exterior por el puerto 80.

## Objetivo

- Ejecutar Django con Gunicorn.
- Enrutar trafico HTTP por Nginx.
- Dejar la base para implementar Strangler Pattern en rutas futuras.

## Arquitectura

- `db` -> PostgreSQL
- `web` -> Django + Gunicorn (sin puertos expuestos al host)
- `nginx` -> Proxy inverso expuesto en `80:80`

## Ejecutar local

Desde la carpeta `tutorial05_Strangler_Nginx`:

```bash
docker compose up -d --build
docker compose ps
```

Aplicar migraciones:

```bash
docker compose exec web python manage.py migrate
```

Crear datos minimos de prueba:

```bash
docker compose exec web python manage.py shell -c "from tienda_app.models import Libro,Inventario; libro,_=Libro.objects.get_or_create(id=1, defaults={'titulo':'Libro Demo','precio':'50000.00'}); Inventario.objects.update_or_create(libro=libro, defaults={'cantidad':10}); print('OK', libro.id)"
```

Probar API por Nginx (puerto 80):

```bash
curl -X POST http://127.0.0.1/api/v1/comprar/ -H "Content-Type: application/json" -d '{"libro_id":1,"direccion_envio":"Bogota","cantidad":1}'
```

## Despliegue en EC2

```bash
git pull origin main
docker compose up -d --build
docker compose ps
```

Si tu instancia usa `docker-compose` clasico, reemplaza `docker compose` por
`docker-compose` en todos los comandos.

## Security Group en AWS

Abrir regla de entrada:

- Tipo: `HTTP`
- Puerto: `80`
- Source: `0.0.0.0/0`

## Evidencias de entrega

1. Navegador en `http://<IP-EC2>/api/v1/comprar/` sin usar `:8000`.
2. Intento a `http://<IP-EC2>:8000` debe fallar (Django aislado).
3. Captura de `docker ps` en EC2 mostrando `nginx`, `web` y `db` en estado `Up`.

## Logs utiles

```bash
docker compose logs -f nginx
docker compose logs -f web
docker compose logs -f db
```

## Apagar stack

```bash
docker compose down
```
