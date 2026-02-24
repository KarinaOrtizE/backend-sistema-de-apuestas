import random
from src.entities.Juego import Juego
from src.entities.Jugador import Jugador


class RuletaRapida(Juego):

    def __init__(self):
        super().__init__("Ruleta Rápida", 0, 0)

        self.numeros = [
            0,
            32,
            15,
            19,
            4,
            21,
            2,
            25,
            17,
            34,
            6,
            27,
            13,
            36,
            11,
            30,
            8,
            23,
            10,
            5,
            24,
            16,
            33,
            1,
            20,
            14,
            31,
            9,
            22,
            18,
            29,
            7,
            28,
            12,
            35,
            3,
            26,
        ]

        self.rojos = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
        self.negros = {
            2,
            4,
            6,
            8,
            10,
            11,
            13,
            15,
            17,
            20,
            22,
            24,
            26,
            28,
            29,
            31,
            33,
            35,
        }

        self.apuesta_actual = None
        self.monto_actual = 0
        self.historial = []

    def comprar_boleto(self, jugador: Jugador) -> bool:

        while True:
            print("\n--- RULETA RÁPIDA ---")
            print("Saldo actual:", jugador.saldo)
            print("1. Rojo")
            print("2. Negro")
            print("3. Par")
            print("4. Impar")
            print("5. 1-18 (Falta)")
            print("6. 19-36 (Pasa)")
            print("7. Número exacto (0-36)")

            opcion = input("Seleccione su apuesta: ")

            if opcion not in ["1", "2", "3", "4", "5", "6", "7"]:
                print("Opción inválida.")
                continue

            try:
                monto = float(input("Ingrese monto a apostar: "))
            except:
                print("Monto inválido.")
                continue

            if monto <= 0:
                print("El monto debe ser mayor a 0.")
                continue

            if jugador.saldo < monto:
                print("Saldo insuficiente.")
                return False

            jugador.saldo -= monto
            self.monto_actual = monto

            if opcion == "1":
                self.apuesta_actual = "rojo"
            elif opcion == "2":
                self.apuesta_actual = "negro"
            elif opcion == "3":
                self.apuesta_actual = "par"
            elif opcion == "4":
                self.apuesta_actual = "impar"
            elif opcion == "5":
                self.apuesta_actual = "falta"
            elif opcion == "6":
                self.apuesta_actual = "pasa"
            elif opcion == "7":
                while True:
                    try:
                        numero = int(input("Elija número (0-36): "))
                        if 0 <= numero <= 36:
                            self.apuesta_actual = numero
                            break
                        else:
                            print("Número fuera de rango.")
                    except:
                        print("Entrada inválida.")
            break

        return True

    def ejecutar_sorteo(self):

        resultado = random.choice(self.numeros)

        if resultado == 0:
            color = "Verde"
        elif resultado in self.rojos:
            color = "Rojo"
        else:
            color = "Negro"

        print("\n Girando ruleta...")
        print(f"Resultado: {resultado} - {color}")

        return resultado

    def calcular_premio(self, jugador: Jugador, resultado):

        gano = False
        premio = 0

        if resultado == 0 and self.apuesta_actual == 0:
            premio = self.monto_actual * 18
            gano = True

        elif resultado != 0:

            if self.apuesta_actual == "rojo" and resultado in self.rojos:
                premio = self.monto_actual * 2
                gano = True

            elif self.apuesta_actual == "negro" and resultado in self.negros:
                premio = self.monto_actual * 2
                gano = True

            elif self.apuesta_actual == "par" and resultado % 2 == 0:
                premio = self.monto_actual * 2
                gano = True

            elif self.apuesta_actual == "impar" and resultado % 2 != 0:
                premio = self.monto_actual * 2
                gano = True

            elif self.apuesta_actual == "falta" and 1 <= resultado <= 18:
                premio = self.monto_actual * 2
                gano = True

            elif self.apuesta_actual == "pasa" and 19 <= resultado <= 36:
                premio = self.monto_actual * 2
                gano = True

            elif (
                isinstance(self.apuesta_actual, int)
                and resultado == self.apuesta_actual
            ):
                premio = self.monto_actual * 18
                gano = True

        if gano:
            jugador.saldo += premio
            mensaje = f" Ganaste {premio}. Nuevo saldo: {jugador.saldo}"
        else:
            mensaje = f" Perdiste. Saldo actual: {jugador.saldo}"

        self.historial.append(
            {
                "apuesta": self.apuesta_actual,
                "resultado": resultado,
                "monto": self.monto_actual,
                "ganancia": premio,
            }
        )

        print(mensaje)
        return mensaje

    def mostrar_historial(self):
        print("\n===== HISTORIAL =====")
        if not self.historial:
            print("No hay jugadas registradas.")
            return

        for i in range(len(self.historial)):
            jugada = self.historial[i]
            print(
                f"Ronda {i+1} -> "
                f"Apuesta: {jugada['apuesta']} | "
                f"Resultado: {jugada['resultado']} | "
                f"Monto: {jugada['monto']} | "
                f"Ganancia: {jugada['ganancia']}"
            )
