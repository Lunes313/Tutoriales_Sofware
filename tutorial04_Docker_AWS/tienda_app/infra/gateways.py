import datetime
from ..domain.interfaces import ProcesadorPago

class BancoNacionalProcesador(ProcesadorPago):
    """
    Implementación concreta de la infraestructura.
    Simula un banco local escribiendo en un log.
    """
    def pagar(self, monto: float) -> bool:
        archivo_log = 'pagos_locales_Laura_Restrepo.log'

        with open(archivo_log, 'a', encoding='utf-8') as archivo:
            archivo.write(f"[{datetime.datetime.now()}] Transaccion exitosa por: ${monto}\n")
        return True