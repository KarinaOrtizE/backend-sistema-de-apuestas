from datetime import date
from src.entities.Jugador import Jugador
from src.entities.Billetera import Billetera


class Main:

    EDAD_MINIMA = 18

    def __init__(self) -> None:
        self._jugadores: dict[int, Jugador] = {}
        self._billeteras: dict[int, Billetera] = {}

    def menu_principal(self) -> None:
        while True:
            print("\n===== BIENVENIDO AL SISTEMA DE APUESTAS =====")
            print("\nAntes de jugar, debes crear o iniciar sesión en tu cuenta.")
            print("1. Ingresar a cuenta")
            print("2. Crear cuenta")
            print("0. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self.iniciar_sesion()
            elif opcion == "2":
                self.crear_cuenta()
            elif opcion == "0":
                print("Gracias por usar nuestro sistema.")
                break
            else:
                print("Opción no disponible.")

    def iniciar_sesion(self) -> None:
        print("\nINICIAR SESIÓN")

        nombre = input("Nombre: ")
        documento = int(input("Cédula: "))

        if documento not in self._jugadores:
            print("Usuario no encontrado.")
            return

        jugador = self._jugadores[documento]

        if jugador.nombre != nombre:
            print("Nombre incorrecto.")
            return

        print(f"Bienvenido {jugador.nombre}")
        self._menu_usuario(documento)

    def crear_cuenta(self) -> None:
        print("\nCREAR CUENTA")

        nombre = input("Nombre completo: ")
        documento = int(input("Cédula: "))
        correo = input("Correo: ")

        ano = int(input("Año de nacimiento: "))
        mes = int(input("Mes de nacimiento: "))
        dia = int(input("Día de nacimiento: "))

        fecha_nacimiento = date(ano, mes, dia)

        if not self._es_mayor_de_edad(fecha_nacimiento):
            print("Debes ser mayor de edad para crear una cuenta.")
            return

        if documento in self._jugadores:
            print("Ya existe una cuenta con esa cédula, intenta iniciar sesión.")
            return

        jugador = Jugador(nombre, documento, correo, fecha_nacimiento)
        billetera = Billetera()

        self._jugadores[documento] = jugador
        self._billeteras[documento] = billetera

        print("Tu cuenta se creó de forma exitosa. Ahora debe iniciar sesión.")


if __name__ == "__main__":
    app = Main()
    app.menu_principal()
