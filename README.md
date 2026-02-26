🎰 Sistema de Juegos de Azar en Python

Proyecto desarrollado en Python que simula un sistema de juegos de azar con manejo de jugadores, billetera y diferentes modalidades de juego.

📌 Descripción

Este sistema permite a un jugador registrarse, depositar dinero en su billetera y participar en distintos juegos de azar:

🎡 Ruleta Rápida

🎟 Lotería

🎱 Bingo (5x5)

Cada juego tiene su propia lógica de apuesta, validaciones y cálculo de premios, pero todos siguen una estructura orientada a objetos.

🏗 Arquitectura del Proyecto

El sistema está construido bajo el paradigma de Programación Orientada a Objetos (POO).

📂 Estructura de Clases

Juego → Clase base abstracta.

Jugador → Representa al usuario del sistema.

Billetera → Administra el saldo del jugador.

RuletaRapida → Juego de apuesta por color o número.

Loteria → Juego de selección de 4 números.

Bingo → Cartón 5x5 con meta de aciertos.

main.py → Archivo principal que ejecuta el sistema.

🎮 Juegos Implementados
🎡 Ruleta Rápida

Apuesta por:

Número (0–36)

Color (rojo o negro)

Multiplicadores:

Número exacto → x35

Color → x2

🎟 Lotería

El jugador elige 4 números entre 0 y 9.

Se genera un número ganador aleatorio.

Si coincide exactamente, gana el premio acumulado.

🎱 Bingo

Genera un cartón 5x5 automático.

El centro es espacio libre.

Se sortean 25 balotas del 1 al 75.

El jugador gana al alcanzar una meta de aciertos definida.

💰 Sistema de Billetera

Cada jugador tiene una billetera que permite:

➕ Depositar saldo

➖ Descontar apuestas

🏆 Recibir premios

Validaciones incluidas:

No permite apostar sin saldo suficiente.

No permite valores negativos.

Validación lógica de entradas.

⚙️ Características Técnicas

✔ Programación Orientada a Objetos

✔ Uso de tipado estático (type hints)

✔ Validaciones lógicas sin abuso de try/except

✔ Generación aleatoria con random

✔ Simulación dinámica con time.sleep

✔ Modularización en múltiples archivos

✔ Documentación con docstrings

▶️ Cómo Ejecutar el Proyecto

Asegúrese de tener Python 3.10+

Ubíquese en la carpeta raíz del proyecto.

Ejecute:

python main.py
🧠 Conceptos Aplicados

Clases y objetos

Encapsulamiento

Herencia (clase base Juego)

Modularización

Validación de datos

Lógica condicional

Listas y matrices

Manejo de atributos de instancia

📈 Posibles Mejoras Futuras

Implementar historial de partidas

Agregar persistencia en archivo o base de datos

Implementar interfaz gráfica (Tkinter o web)

Agregar más tipos de apuestas

Implementar patrones de diseño (Factory, Strategy)
