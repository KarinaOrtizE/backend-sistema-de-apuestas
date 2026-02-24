from datetime import date


class Jugador:
    def __init__(
        self, nombre: str, documento: int, correo: str, fecha_nacimiento: date
    ) -> None:
        self._nombre = nombre.strip()
        self._documento = documento
        self._correo = correo.strip()
        self._fecha_nacimiento = fecha_nacimiento

    @property
    def nombre(self):
        return self._nombre

    @property
    def documento(self):
        return self._documento

    @property
    def correo(self):
        return self._correo

    @property
    def fecha_nacimiento(self):
        return self._fecha_nacimiento

    def __str__(self):
        return f"{self._nombre} - {self._documento}"


def registrar_jugador() -> Jugador:
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
