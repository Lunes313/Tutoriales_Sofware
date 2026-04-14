from .models import Inventario, Libro, Orden


class CalculadorImpuestos:
    IVA = 1.19

    @staticmethod
    def obtener_total_con_iva(precio):
        return float(precio) * CalculadorImpuestos.IVA


class CompraRapidaService:
    def __init__(self, procesador_pago):
        self.procesador_pago = procesador_pago

    def procesar(self, libro_id):
        libro = Libro.objects.get(id=libro_id)
        inventario = Inventario.objects.filter(libro=libro).first()

        if inventario is None:
            raise ValueError('El libro no tiene inventario registrado.')

        if inventario.cantidad <= 0:
            raise ValueError('No hay existencias.')

        total = CalculadorImpuestos.obtener_total_con_iva(libro.precio)

        if self.procesador_pago.pagar(total):
            inventario.cantidad -= 1
            inventario.save()
            Orden.objects.create(libro=libro, total=total)
            return total

        return None
