"""Módulo que implementa el juego Ruleta Rápida.

Permite a un jugador realizar apuestas simples (color, paridad o rango),
ejecutar el sorteo, calcular premios y mantener un historial de jugadas.

Regla especial:
    - Si el resultado es 0, el jugador recibe la mitad del monto apostado.
"""

import random
from src.entities.Juego import Juego
from src.entities.Jugador import Jugador


class RuletaRapida(Juego):
    """Representa el juego Ruleta Rápida.

    Hereda de la clase Juego e implementa la lógica específica
    para apuestas simples y cálculo de premios.
    """

    def __init__(self) -> None:
        """Inicializa la ruleta con números, colores y estado interno."""
        super().__init__("Ruleta Rápida", 0, 0)

        self.numeros: list[int] = [
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

        self.rojos: set[int] = {
            1,
            3,
            5,
            7,
            9,
            12,
            14,
            16,
            18,
            19,
            21,
            23,
            25,
            27,
            30,
            32,
            34,
            36,
        }

        self.negros: set[int] = {
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

        self.apuesta_actual: str | None = None
        self.monto_actual: float = 0.0
        self.historial: list[dict] = []

    def comprar_boleto(self, jugador: Jugador) -> bool:
        """Permite al jugador seleccionar una apuesta válida y descontar
        el monto desde su billetera.

        Parámetros:
            jugador (Jugador): Jugador que realiza la apuesta.

        Retorna:
            bool: True si la apuesta fue registrada correctamente.
                  False si hubo error de validación o saldo insuficiente.
        """
        print("\n--- RULETA RÁPIDA ---")
        print(jugador.billetera.mostrar_saldo())
        print("1. Rojo")
        print("2. Negro")
        print("3. Par")
        print("4. Impar")
        print("5. 1-18 (Falta)")
        print("6. 19-36 (Pasa)")

        opcion: str = input("Seleccione su apuesta: ")

        if opcion not in ["1", "2", "3", "4", "5", "6"]:
            print("Opción inválida.")
            return False

        monto_texto: str = input("Ingrese monto a apostar: ")

        try:
            monto: float = float(monto_texto)
        except ValueError:
            print("Monto inválido.")
            return False

        if monto <= 0:
            print("El monto debe ser mayor a 0.")
            return False

        if not jugador.billetera.descontar_saldo(monto):
            print("Saldo insuficiente.")
            return False

        self.monto_actual = monto

        opciones = {
            "1": "rojo",
            "2": "negro",
            "3": "par",
            "4": "impar",
            "5": "falta",
            "6": "pasa",
        }

        self.apuesta_actual = opciones[opcion]

        return True

    def ejecutar_sorteo(self) -> int:
        """Realiza el sorteo de la ruleta seleccionando un número aleatorio.

        Retorna:
            int: Número resultante del giro.
        """
        resultado: int = random.choice(self.numeros)

        if resultado == 0:
            color = "Verde"
        elif resultado in self.rojos:
            color = "Rojo"
        else:
            color = "Negro"

        print("\nGirando ruleta...")
        print(f"Resultado: {resultado} - {color}")

        return resultado

    def calcular_premio(self, jugador: Jugador, resultado: int) -> str:
        """Evalúa el resultado del sorteo y gestiona el pago del premio
        utilizando la billetera del jugador.

        Reglas:
            - Si el resultado es 0, se devuelve la mitad del monto apostado.
            - Si gana, se deposita el premio en la billetera.
            - Si pierde, no se devuelve dinero.

        Parámetros:
            jugador (Jugador): Jugador que realizó la apuesta.
            resultado (int): Número obtenido en el sorteo.

        Retorna:
            str: Mensaje descriptivo del resultado.
        """
        premio: float = 0.0
        gano: bool = False

        if resultado == 0:
            premio = self.monto_actual / 2
            gano = True
        else:
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

        if gano:
            jugador.billetera.sumar_saldo(premio)
            mensaje = f"Ganaste ${premio}. {jugador.billetera.mostrar_saldo()}"
        else:
            mensaje = f"Perdiste la apuesta. {jugador.billetera.mostrar_saldo()}"

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

    def mostrar_historial(self) -> None:
        """Muestra el historial de jugadas realizadas durante la sesión."""
        print("\n===== HISTORIAL =====")

        if not self.historial:
            print("No hay jugadas registradas.")
            return

        for i, jugada in enumerate(self.historial, start=1):
            print(
                f"Ronda {i} -> "
                f"Apuesta: {jugada['apuesta']} | "
                f"Resultado: {jugada['resultado']} | "
                f"Monto: {jugada['monto']} | "
                f"Ganancia: {jugada['ganancia']}"
            )
