from decimal import Decimal

from .logic import CalculadorImpuestos
from ..models import Orden


class OrdenBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        self._usuario = None
        self._items = []
        self._direccion = ""

    def con_usuario(self, usuario):
        self._usuario = usuario
        return self

    def con_productos(self, productos):
        self._items = productos
        return self

    def para_envio(self, direccion):
        self._direccion = direccion
        return self

    def build(self) -> Orden:
        if not self._items:
            raise ValueError("Datos insuficientes para crear la orden.")

        subtotal = sum(Decimal(item.precio) for item in self._items)
        total = Decimal(CalculadorImpuestos.obtener_total_con_iva(subtotal))
        libro_principal = self._items[0]

        orden = Orden.objects.create(
            usuario=self._usuario,
            libro=libro_principal,
            total=total,
            direccion_envio=self._direccion,
        )
        self.reset()
        return orden
