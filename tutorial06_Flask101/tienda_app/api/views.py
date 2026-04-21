from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from tienda_app.infra.factories import PaymentFactory
from tienda_app.models import Libro
from tienda_app.services import CompraService


class ProductosAPIView(APIView):
    """
    Endpoint v1 - Sirve desde Django (monolito).
    GET /api/v1/productos/
    """
    def get(self, request):
        libros = Libro.objects.all().values('id', 'titulo', 'precio')
        return Response({
            "servidor": "Django v1 (monolito)",
            "productos": list(libros)
        })


class CompraAPIView(APIView):
    """
    Endpoint v1 - Compras procesadas por Django.
    POST /api/v1/comprar/
    Payload: {"libro_id": 1, "direccion_envio": "Calle 123", "cantidad": 1}
    """
    def post(self, request):
        libro_id = request.data.get('libro_id')
        direccion = request.data.get('direccion_envio', '')
        cantidad = request.data.get('cantidad', 1)

        if not libro_id:
            return Response(
                {"error": "El campo libro_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST
            )

        gateway = PaymentFactory.get_processor()
        servicio = CompraService(procesador_pago=gateway)

        try:
            total = servicio.ejecutar_compra(
                libro_id=libro_id,
                direccion=direccion,
                usuario=request.user if request.user.is_authenticated else None,
                cantidad=cantidad,
            )
            return Response(
                {"estado": "exito", "mensaje": f"Orden creada. Total: {total}"},
                status=status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)