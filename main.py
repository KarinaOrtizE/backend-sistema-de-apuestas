from datetime import datetime
from src.entities.Jugador import Jugador


class Main:

    def __init__(self) -> None:
        self._jugadores: dict[str, Jugador] = {}

    def menu_principal(self) -> None:
        while True:
            print("\n===== BIENVENIDO AL SISTEMA DE APUESTAS =====")
            print("\nAntes de jugar, debes crear o iniciar sesión en tu cuenta.")
            print("1. Ingresar a cuenta")
            print("2. Crear cuenta")
            print("0. Salir")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                self._ingresar_cuenta()
            elif opcion == "2":
                self._crear_cuenta()
            elif opcion == "0":
                print("Gracias por usar nuestro sistema.")
                break
            else:
                print("Opción no disponible.")

    def _ingresar_cuenta(self) -> None:
        print("\n===== INICIAR SESIÓN =====")

    def _crear_cuenta(self) -> None:
        print("\n===== CREAR CUENTA =====")

        nombre = input("Nombre completo: ")
        cedula = input("Cédula: ")
        fecha_str = input("Fecha nacimiento (YYYY-MM-DD): ")

        if cedula in self._jugadores:
            print("Ya existe un usuario con esa cédula.")
            return

        fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()

        jugador = Jugador(nombre, cedula, fecha)

        if not jugador.es_mayor_de_edad():
            print("Debe ser mayor de edad.")
            return

        self._jugadores[cedula] = jugador
        print("Cuenta creada correctamente.")


if __name__ == "__main__":
    app = Main()
    app.menu_principal()
