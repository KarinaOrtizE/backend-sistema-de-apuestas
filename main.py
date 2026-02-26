from datetime import date
from src.entities.Jugador import Jugador, registrar_jugador
from src.entities.Billetera import Billetera
from src.entities.Ruleta import RuletaRapida


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
        self.menu_usuario(documento)

    def crear_cuenta(self) -> None:
        print("\nCREAR CUENTA")

        jugador = registrar_jugador()

        if not self.es_mayor_de_edad(jugador.fecha_nacimiento):
            print("Debes ser mayor de edad para crear una cuenta en nuestro sistema.")
            return

        if jugador.documento in self._jugadores:
            print("Ya existe una cuenta con esa cédula, intenta iniciar sesión.")
            return

        billetera = Billetera()

        self._jugadores[jugador.documento] = jugador
        self._billeteras[jugador.documento] = billetera

        print("Tu cuenta se creó de forma exitosa. Ahora debes iniciar sesión.")

    def es_mayor_de_edad(self, fecha_nacimiento: date) -> bool:
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year

        if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
            edad -= 1

        return edad >= self.EDAD_MINIMA

    def menu_usuario(self, documento: int) -> None:
        billetera = self._billeteras[documento]

        while True:
            print("\nMENÚ USUARIO")
            print("1. Recargar saldo")
            print("2. Visualizar saldo")
            print("3. Jugar")
            print("0. Cerrar sesión")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                monto = float(input("Ingrese monto a recargar: "))

                if billetera.recargar(monto):
                    print("Recarga exitosa.")
                else:
                    print(
                        "Monto inválido. Para jugar en nuestro sistema debes de temer saldo disponible."
                    )

            elif opcion == "2":
                print(billetera.mostrar_saldo())

            elif opcion == "3":

                if billetera.saldo <= 0:
                    print("Debe recargar saldo antes de poder jugar.")
                else:
                    self.menu_juegos()

            elif opcion == "0":
                print("Sesión cerrada.")
                break
            else:
                print("Opción no disponible.")

    def menu_juegos(self) -> None:
        while True:
            print("\nMENÚ DE JUEGOS")
            print("1. Ruleta")
            print("2. Bingo")
            print("3. Lotería")
            print("0. Volver")

            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                # Ruleta
                print("Entrando a Ruleta...")
            elif opcion == "2":
                # Bingo
                print("Entrando a Bingo...")
            elif opcion == "3":
                # Loteria
                print("Entrando a Lotería...")
            elif opcion == "0":
                break
            else:
                print("Opción no disponible.")


if __name__ == "__main__":
    app = Main()
    app.menu_principal()
