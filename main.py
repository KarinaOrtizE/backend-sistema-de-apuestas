from datetime import datetime
from entities.jugador import Jugador


class Main:

    def __init__(self) -> None:
        self._jugadores: dict[str, Jugador] = {}

    def menu_principal(self) -> None:
        while True:
            print("\n===== BIENVENIDO AL SISTEMA DE APUESTAS =====")
            print("\nAntes de jugar, debes crear o iniciar sesión en tu cuenta.")
            print("1. Crear cuenta")
            print("2. Ingresar a cuenta")
            print("0. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self._crear_cuenta()
            elif opcion == "2":
                self._ingresar_cuenta()
            elif opcion == "0":
                print("Gracias por usar nuestro sistema.")
                break
            else:
                print("Opción no disponible.")


if __name__ == "__main__":
    app = Main()
    app.menu_principal()
