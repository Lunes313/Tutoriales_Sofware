import datetime

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from .models import Inventario, Libro, Orden


def compra_rapida_fbv(request, libro_id):
    libro = get_object_or_404(Libro, id=libro_id)

    if request.method == 'POST':
        inventario = get_object_or_404(Inventario, libro=libro)
        if inventario.cantidad > 0:
            total = float(libro.precio) * 1.19
            with open('pagos_locales_Laura_Restrepo.log', 'a', encoding='utf-8') as archivo:
                archivo.write(f"[{datetime.datetime.now()}] Pago FBV: ${total}\n")
            inventario.cantidad -= 1
            inventario.save()
            Orden.objects.create(libro=libro, total=total)
            return HttpResponse(f'Compra exitosa: {libro.titulo}')
        return HttpResponse('Sin stock', status=400)

    total_estimado = float(libro.precio) * 1.19
    return render(
        request,
        'tienda_app/compra_rapida.html',
        {
            'libro': libro,
            'total': total_estimado,
        },
    )


class CompraRapidaView(View):
    template_name = 'tienda_app/compra_rapida.html'

    def get(self, request, libro_id):
        libro = get_object_or_404(Libro, id=libro_id)
        total = float(libro.precio) * 1.19
        return render(
            request,
            self.template_name,
            {
                'libro': libro,
                'total': total,
            },
        )

    def post(self, request, libro_id):
        from tienda_app.infra.gateways import BancoNacionalProcesador
        from tienda_app.services import CompraRapidaService

        servicio = CompraRapidaService(BancoNacionalProcesador())
        try:
            total = servicio.procesar(libro_id)
            return HttpResponse(f'Comprado via CBV: ${total}')
        except ValueError as error:
            return HttpResponse(str(error), status=400)
