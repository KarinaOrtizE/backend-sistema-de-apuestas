from typing import List, Any
import random
from src.entities.Juego import Juego
from src.entities.Jugador import Jugador


class Loteria(Juego):
    def __init__(self):
        super().__init__(nombre="Lotería 4 Cifras", costo=50000, recompensa=500000)
        self.numeros_jugador: List[int] = []
        self.numeros_ganadores: List[int] = []

        self.digitos = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

    def comprar_boleto(self, jugador: Jugador) -> bool:

        print(f"\n {self.nombre}")
        print("=" * 40)
        print(f"Jugador: {jugador.nombre}")

        if not Jugador.billetera.descontar_saldo(self.costo):
            print(f" No tienes suficiente saldo. Necesitas ${self.costo:,}")
            print(f" {Jugador.billetera.mostrar_saldo()}")
            return False

        print(f"Costo del juego: ${self.costo:,}")
        print(f"{Jugador.billetera.mostrar_saldo()}")
        print("\n Debes ingresar un número de 4 cifras (cada cifra del 0-9)")

        return True

    def validar_numero(self, numero_ingresado: str) -> bool:

        if len(numero_ingresado) != 4:
            print(" Debes ingresar 4 dígitos.")
            return False

        for caracter in numero_ingresado:
            if caracter not in self.digitos:
                print(" Solo puedes ingresar números.")
                return False

        return True

    def obtener_numeros_jugador(self) -> List[int]:

        while True:
            numero_ingresado = input(" Ingresa un número de 4 cifras: ")

            if self.validar_numero(numero_ingresado):
                numeros = []

                for caracter in numero_ingresado:

                    posicion = self.digitos.index(caracter)
                    numeros.append(posicion)

                return numeros

    def ejecutar_sorteo(self) -> List[int]:

        self.numeros_ganadores = []

        for i in range(4):
            numero = random.randint(1, 9)
            self.numeros_ganadores.append(numero)

        return self.numeros_ganadores

    def calcular_premio(self, jugador: Jugador, resultado: List[int]) -> str:

        print("\n" + "=" * 40)
        print(" RESULTADOS")
        print("=" * 40)
        print(f" Tus números:     {self.numeros_jugador}")
        print(f" Números ganadores: {resultado}")

        if self.numeros_jugador == resultado:
            # agregar la recompensa a la billetera
            # jugador.billetera.agregar(self.recompensa)
            mensaje = (
                f"\n ¡FELICIDADES {jugador.nombre}! ¡HAS GANADO!\n"
                f" ¡Acertaste todos los números en el orden correcto!\n"
                f" Premio: ${self.recompensa:,}"
            )
        else:
            # Verificar aciertos por posición
            aciertos = 0
            aciertos_posiciones = []

            # Comparamos posición por posición
            for i in range(4):
                if self.numeros_jugador[i] == resultado[i]:
                    aciertos += 1
                    aciertos_posiciones.append(str(i + 1))

            mensaje = f"\n Lo siento {jugador.nombre}, has perdido."

        # mostrar el saldo actual
        # mensaje += f"\n\n Saldo actual: ${jugador.billetera.consultar_saldo():,}"

        return mensaje

    def jugar(self, jugador: Jugador) -> bool:
        """Método principal para jugar a la lotería"""
        # Paso 1: Comprar boleto (validar fondos)
        if not self.comprar_boleto(jugador):
            return False

        # Paso 2: Obtener números del jugador
        self.numeros_jugador = self.obtener_numeros_jugador()

        # Paso 3: Ejecutar sorteo
        numeros_ganadores = self.ejecutar_sorteo()

        # Paso 4: Calcular premio
        resultado = self.calcular_premio(jugador, numeros_ganadores)
        print(resultado)

        return True
