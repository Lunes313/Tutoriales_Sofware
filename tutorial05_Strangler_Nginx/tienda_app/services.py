from .domain.builders import OrdenBuilder
from .domain.logic import CalculadorImpuestos
from .models import Inventario, Libro


class CompraService:
    def __init__(self, procesador_pago):
        self.procesador = procesador_pago
        self.builder = OrdenBuilder()

    def obtener_detalle_producto(self, libro_id):
        libro = Libro.objects.get(id=libro_id)
        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)
        return {'libro': libro, 'total': total}

    def ejecutar_compra(self, libro_id, direccion, usuario=None, cantidad=1):
        libro = Libro.objects.get(id=libro_id)
        inventario = Inventario.objects.filter(libro=libro).first()

        if inventario is None:
            raise ValueError(f'El libro {libro.titulo} no tiene inventario registrado.')

        if cantidad <= 0:
            raise ValueError('La cantidad debe ser mayor que cero.')

        if inventario.cantidad < cantidad:
            raise ValueError(f'No hay existencias suficientes para {libro.titulo}.')

        lista_productos = [libro for _ in range(cantidad)]

        orden = (
            self.builder
            .con_usuario(usuario)
            .con_productos(lista_productos)
            .para_envio(direccion)
            .build()
        )

        if self.procesador.pagar(orden.total):
            inventario.cantidad -= cantidad
            inventario.save()
            return orden.total

        orden.delete()
        raise Exception('Error en la pasarela de pagos.')

    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
        if not lista_productos:
            raise ValueError('Debe seleccionar al menos un producto.')

        return self.ejecutar_compra(
            libro_id=lista_productos[0].id,
            direccion=direccion,
            usuario=usuario,
            cantidad=len(lista_productos),
        )
