"""
Módulo que define la clase Jugador y la función para su registro.

Contiene la representación de un jugador del sistema, incluyendo
sus datos personales y la lógica para crearlo mediante entrada
por consola.
"""

from datetime import date
from .Billetera import Billetera


class Jugador:
    """Representa un jugador del sistema con su información básica."""

    def __init__(
        self, nombre: str, documento: int, correo: str, fecha_nacimiento: date
    ) -> None:
        """Inicializa un jugador con sus datos personales."""
        self._nombre = nombre.strip()
        self._documento = documento
        self._correo = correo.strip()
        self._fecha_nacimiento = fecha_nacimiento
        self._billetera: Billetera = Billetera()

    @property
    def nombre(self):
        """Devuelve el nombre del jugador."""
        return self._nombre

    @property
    def billetera(self):
        """Devuelve la billetera del jugador."""
        return self._billetera

    @property
    def documento(self):
        """Devuelve el documento del jugador."""
        return self._documento

    @property
    def correo(self):
        """Devuelve el correo del jugador."""
        return self._correo

    @property
    def fecha_nacimiento(self):
        """Devuelve la fecha de nacimiento del jugador."""
        return self._fecha_nacimiento

    def __str__(self):
        """Retorna una representación en texto del jugador."""
        return f"{self._nombre} - {self._documento}"


def registrar_jugador() -> Jugador:
    """Solicita los datos por consola y crea un nuevo jugador."""
    nombre = input("Ingrese nombre: ")
    documento = int(input("Ingrese documento: "))
    correo = input("Ingrese correo: ")

    ano: int = int(input("Ingrese año de nacimiento: "))
    mes: int = int(input("Ingrese mes de nacimiento: "))
    dia: int = int(input("Ingrese día de nacimiento: "))

    fecha_nacimiento = date(ano, mes, dia)

    jugador = Jugador(nombre, documento, correo, fecha_nacimiento)
    print("Jugador registrado exitosamente.")
    return jugador


##borrar325252345
