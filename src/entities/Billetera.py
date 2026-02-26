class Billetera:

    def __init__(self) -> None:
        self._saldo: float = 0.0

    @property
    def saldo(self) -> float:
        return self._saldo

    def recargar(self, monto: float) -> bool:
        if monto <= 0:
            return False

        self._saldo += monto
        return True

    def mostrar_saldo(self) -> str:
        return f"Saldo actual: ${self._saldo}"

    def descontar_saldo(self, monto: float) -> bool:
        if monto <= 0:
            return False

        if self._saldo >= monto:
            self._saldo -= monto
            return True

        return False

    def sumar_saldo(self, monto: float) -> bool:
        if monto <= 0:
            return False

        self._saldo += monto
        return True
