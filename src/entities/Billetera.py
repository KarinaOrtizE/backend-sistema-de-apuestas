class Billetera:
    """
    Representa la billetera virtual de un jugador.

    Gestiona el saldo disponible para realizar apuestas,
    permitiendo recargas, descuentos y consultas.
    """

    def __init__(self) -> None:
        """
        Inicializa la billetera con saldo en cero.
        """
        self._saldo: float = 0.0

    @property
    def saldo(self) -> float:
        """
        Retorna el saldo actual disponible en la billetera.
        """
        return self._saldo

    def recargar(self, monto: float) -> bool:
        """
        Recarga saldo en la billetera.

        Parámetros:
            monto (float): Cantidad de dinero a agregar.

        Retorna:
            True si la recarga fue exitosa.
            False si el monto es inválido (menor o igual a cero).
        """
        if monto <= 0:
            return False

        self._saldo += monto
        return True

    def mostrar_saldo(self) -> str:
        """
        Devuelve una representación en texto del saldo actual.

        Retorna:
            str: Mensaje con el saldo disponible.
        """
        return f"Saldo actual: ${self._saldo}"

    def descontar_saldo(self, monto: float) -> bool:
        """
        Descuenta un monto del saldo disponible.

        Parámetros:
            monto (float): Cantidad de dinero a descontar.

        Retorna:
            True si el descuento fue exitoso.
            False si el monto es inválido o no hay saldo suficiente.
        """
        if monto <= 0:
            return False

        if self._saldo >= monto:
            self._saldo -= monto
            return True

        return False

    def sumar_saldo(self, monto: float) -> bool:
        """
        Suma un monto al saldo actual (por ejemplo, ganancias).

        Parámetros:
            monto (float): Cantidad de dinero a agregar.

        Retorna:
            True si la operación fue exitosa.
            False si el monto es inválido.
        """
        if monto <= 0:
            return False

        self._saldo += monto
        return True
