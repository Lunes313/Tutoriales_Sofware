from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from .infra.factories import PaymentFactory
from .models import Libro
from .services import CompraService


class CompraView(View):
    template_name = 'tienda_app/compra_rapida.html'

    def setup_service(self):
        gateway = PaymentFactory.get_processor()
        return CompraService(procesador_pago=gateway)

    def get(self, request, libro_id):
        servicio = self.setup_service()
        contexto = servicio.obtener_detalle_producto(libro_id)
        return render(request, self.template_name, contexto)

    def post(self, request, libro_id):
        servicio = self.setup_service()
        usuario = request.user if request.user.is_authenticated else None

        try:
            total = servicio.ejecutar_compra(
                libro_id=libro_id,
                direccion='Sin direccion',
                usuario=usuario,
                cantidad=1,
            )
            return HttpResponse(f'Compra exitosa. Total: {total}')
        except ValueError as error:
            return HttpResponse(str(error), status=400)
        except Exception as error:
            return HttpResponse(str(error), status=500)
