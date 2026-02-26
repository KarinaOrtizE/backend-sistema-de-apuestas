from datetime import date
from src.entities.Jugador import Jugador, registrar_jugador
from src.entities.Billetera import Billetera
from src.entities.Ruleta import RuletaRapida
from src.entities.Bingo import Bingo
from src.entities.Loteria import Loteria


class Main:
    """
    Clase principal del sistema de apuestas.
    Se encarga de gestionar el flujo del programa,
    autenticación de usuarios y acceso a juegos.
    """

    EDAD_MINIMA = 18

    def __init__(self) -> None:
        """
        Inicializa las estructuras principales del sistema:
        - Diccionario de jugadores registrados.
        - Diccionario de billeteras asociadas a cada jugador.
        """
        self._jugadores: dict[int, Jugador] = {}

    def menu_principal(self) -> None:
        """
        Muestra el menú principal del sistema.

        Permite:
        - Iniciar sesión.
        - Crear una cuenta nueva.
        - Salir del sistema.
        """
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
        """
        Permite a un usuario autenticarse en el sistema
        validando nombre y documento.

        Si la autenticación es exitosa, accede al menú
        de usuario correspondiente.
        """
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
        """
        Registra un nuevo jugador en el sistema.

        Valida:
        - Que sea mayor de edad.
        - Que no exista previamente una cuenta con el mismo documento.

        Si todo es correcto, crea también una billetera asociada.
        """
        print("\nCREAR CUENTA")

        jugador = registrar_jugador()

        if not self.es_mayor_de_edad(jugador.fecha_nacimiento):
            print("Debes ser mayor de edad para crear una cuenta en nuestro sistema.")
            return

        if jugador.documento in self._jugadores:
            print("Ya existe una cuenta con esa cédula, intenta iniciar sesión.")
            return

        self._jugadores[jugador.documento] = jugador

        print("Tu cuenta se creó de forma exitosa. Ahora debes iniciar sesión.")

    def es_mayor_de_edad(self, fecha_nacimiento: date) -> bool:
        """
        Calcula si una persona es mayor de edad
        comparando su fecha de nacimiento con la fecha actual.

        Retorna:
            True si tiene 18 años o más.
            False en caso contrario.
        """
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year

        if (hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day):
            edad -= 1

        return edad >= self.EDAD_MINIMA

    def menu_usuario(self, documento: int) -> None:
        """
        Muestra el menú del usuario autenticado.

        Permite:
        - Recargar saldo.
        - Consultar saldo.
        - Acceder al menú de juegos.
        - Cerrar sesión.
        """
        jugador = self._jugadores[documento]
        billetera = jugador.billetera

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
                    self.menu_juegos(documento)

            elif opcion == "0":
                print("Sesión cerrada.")
                break
            else:
                print("Opción no disponible.")

    def menu_juegos(self, documento: int) -> None:
        """
        Muestra el menú de juegos disponibles en el sistema.

        Permite seleccionar entre:
        - Ruleta
        - Bingo
        - Lotería
        """
        jugador = self._jugadores[documento]

        while True:
            print("\nMENÚ DE JUEGOS")
            print("1. Ruleta")
            print("2. Bingo")
            print("3. Lotería")
            print("0. Volver")

            opcion = input("Seleccione una opción: ")
            if opcion == "1":
                print("Entrando a Ruleta...")

                juego_ruleta = RuletaRapida()

                if juego_ruleta.comprar_boleto(jugador):
                    resultado = juego_ruleta.ejecutar_sorteo()
                    juego_ruleta.calcular_premio(jugador, resultado)
                else:
                    print("No se pudo realizar la apuesta.")

            elif opcion == "2":
                print("Entrando a Bingo...")

                juego_bingo = Bingo()

                if juego_bingo.comprar_boleto(jugador):
                    print("Boleto comprado con éxito.")
                    balotas = juego_bingo.ejecutar_sorteo()
                    resultado = juego_bingo.calcular_premio(jugador, balotas)
                    print(resultado)
                else:
                    print("No tienes saldo suficiente para comprar el boleto.")

            elif opcion == "3":
                print("Entrando a Lotería...")
                juego_loteria = Loteria()
                juego_loteria.jugar(jugador)

            elif opcion == "0":
                break

            else:
                print("Opción no disponible.")


if __name__ == "__main__":
    app = Main()
    app.menu_principal()
