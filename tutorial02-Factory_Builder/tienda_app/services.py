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

    def ejecutar_proceso_compra(self, usuario, lista_productos, direccion):
        if not lista_productos:
            raise ValueError('Debe seleccionar al menos un producto.')

        inventarios = []
        for producto in lista_productos:
            inventario = Inventario.objects.filter(libro=producto).first()
            if inventario is None:
                raise ValueError(f'El libro {producto.titulo} no tiene inventario registrado.')
            if inventario.cantidad <= 0:
                raise ValueError(f'No hay existencias para {producto.titulo}.')
            inventarios.append(inventario)

        orden = (
            self.builder
            .con_usuario(usuario)
            .con_productos(lista_productos)
            .para_envio(direccion)
            .build()
        )

        if self.procesador.pagar(orden.total):
            for inventario in inventarios:
                inventario.cantidad -= 1
                inventario.save()
            return f'Orden {orden.id} procesada exitosamente.'

        orden.delete()
        raise Exception('Error en la pasarela de pagos.')
