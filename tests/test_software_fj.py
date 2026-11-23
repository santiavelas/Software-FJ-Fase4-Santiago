"""Pruebas automatizadas para las reglas principales del sistema Software FJ."""

import unittest

from software_fj import (
    Cliente,
    DatoInvalidoError,
    EstadoReserva,
    EstadoReservaError,
    RecursoNoDisponibleError,
    ServicioAsesoria,
    ServicioEquipo,
    ServicioSala,
    SistemaFJ,
)
from software_fj.validaciones import validar_numero_positivo


class PruebasSoftwareFJ(unittest.TestCase):
    """Cada prueba prepara datos independientes para evitar efectos cruzados."""

    def setUp(self):
        self.sistema = SistemaFJ()
        self.cliente = Cliente("CLI-T", "Ana Prueba", "ana@example.com", "3001234567")
        self.sistema.registrar_cliente(self.cliente)
        self.sala = ServicioSala("SAL-T", 50000, 8)
        self.equipo = ServicioEquipo("EQ-T", "Proyector", 20000, 2)
        self.asesoria = ServicioAsesoria("ASE-T", "Python", 100000)
        self.sistema.registrar_servicio(self.sala)
        self.sistema.registrar_servicio(self.equipo)
        self.sistema.registrar_servicio(self.asesoria)

    def test_rechaza_correo_invalido(self):
        with self.assertRaises(DatoInvalidoError):
            Cliente("CLI-X", "Persona", "correo-invalido", "3001234567")

    def test_detecta_cliente_duplicado(self):
        from software_fj import ClienteDuplicadoError
        segundo = Cliente("CLI-T", "Otra persona", "otra@example.com", "3101234567")
        with self.assertRaises(ClienteDuplicadoError):
            self.sistema.registrar_cliente(segundo)

    def test_rechaza_duracion_cero(self):
        with self.assertRaises(DatoInvalidoError):
            self.sistema.crear_reserva("R-0", "CLI-T", "ASE-T", 0, {"tema": "POO"})

    def test_rechaza_capacidad_superior_a_la_sala(self):
        with self.assertRaises(DatoInvalidoError):
            self.sistema.crear_reserva("R-CAP", "CLI-T", "SAL-T", 1, {"personas": 9})

    def test_rechaza_cantidad_de_equipo_superior_al_stock(self):
        with self.assertRaises(RecursoNoDisponibleError):
            self.sistema.crear_reserva("R-STOCK", "CLI-T", "EQ-T", 2, {"cantidad": 3})

    def test_calculo_basico_de_sala(self):
        reserva = self.sistema.crear_reserva("R-BASE", "CLI-T", "SAL-T", 2, {"personas": 4})
        self.assertEqual(reserva.calcular_total(), 100000.0)

    def test_calculo_con_impuesto(self):
        reserva = self.sistema.crear_reserva("R-IMP", "CLI-T", "SAL-T", 2, {"personas": 4})
        self.assertEqual(reserva.calcular_total(impuesto=0.19), 119000.0)

    def test_calculo_con_impuesto_y_descuento(self):
        reserva = self.sistema.crear_reserva("R-DES", "CLI-T", "SAL-T", 2, {"personas": 4})
        self.assertEqual(reserva.calcular_total(0.19, 0.10), 107100.0)

    def test_cancelar_reserva_devuelve_inventario(self):
        reserva = self.sistema.crear_reserva("R-CAN", "CLI-T", "EQ-T", 1, {"cantidad": 1})
        reserva.confirmar()
        self.assertEqual(self.equipo.existencias_disponibles, 1)
        reserva.cancelar()
        self.assertEqual(self.equipo.existencias_disponibles, 2)
        self.assertIs(reserva.estado, EstadoReserva.CANCELADA)

    def test_procesar_reserva_confirmada(self):
        reserva = self.sistema.crear_reserva("R-PROC", "CLI-T", "ASE-T", 1, {"tema": "POO"})
        reserva.confirmar()
        self.assertEqual(reserva.procesar(impuesto=0.19), 119000.0)
        self.assertIs(reserva.estado, EstadoReserva.PROCESADA)

    def test_no_permite_procesar_reserva_pendiente(self):
        reserva = self.sistema.crear_reserva("R-PEND", "CLI-T", "ASE-T", 1, {"tema": "POO"})
        with self.assertRaises(EstadoReservaError):
            reserva.procesar()

    def test_encadenamiento_de_excepciones(self):
        with self.assertRaises(DatoInvalidoError) as contexto:
            validar_numero_positivo("no-es-numero", "tarifa")
        self.assertIsInstance(contexto.exception.__cause__, ValueError)

    def test_inventario_completo_se_puede_procesar(self):
        reserva = self.sistema.crear_reserva("R-ALL", "CLI-T", "EQ-T", 1, {"cantidad": 2})
        reserva.confirmar()
        self.assertEqual(self.equipo.existencias_disponibles, 0)
        self.assertEqual(reserva.procesar(), 40000.0)
        self.assertEqual(self.equipo.existencias_disponibles, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
