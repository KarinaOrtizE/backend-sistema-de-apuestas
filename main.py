import sys
from typing import Optional
from uuid import UUID
from datetime import datetime

sys.path.insert(0, ".")

from src.crud import usuario_crud as crud_usuario
from src.crud import apuesta_crud as crud_apuesta
from src.crud import bingo_crud as crud_bingo
from src.crud import sorteo_crud as crud_sorteo
from src.crud import usuario_crud as crud_usuario
from src.crud import ruleta_crud as crud_ruleta
from src.crud import transaccion_crud as crud_transaccion
from src.crud import metodo_pago_crud as crud_metodo_pago


def leer_texto(mensaje: str, default: str = "") -> str:
    s = input(mensaje).strip()
    return s if s else default


def leer_float(mensaje: str, default: float = 0.0) -> float:
    try:
        return float(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_int(mensaje: str, default: int = 0) -> int:
    try:
        return int(input(mensaje).strip() or default)
    except ValueError:
        return default


def leer_uuid(mensaje: str) -> Optional[UUID]:
    s = input(mensaje).strip()
    if not s:
        return None
    try:
        return UUID(s)
    except ValueError:
        return None


def ingresar_o_crear_usuario():
    if len(crud_usuario.listar_todos()) == 0:
        print("\n--- No hay usuarios ---")
        print("Crea el primero:\n")

        nombre = leer_texto("Nombre: ")
        username = leer_texto("Username: ")
        email = leer_texto("Email: ")
        password = leer_texto("Password: ")

        try:
            crud_usuario.crear_usuario(db, nombre, username, password, email)
            print("Usuario creado. Ahora inicia sesión.\n")
        except Exception as e:
            print("Error:", e)
            return None

    while True:
        print("--- Inicio de sesión ---")
        username = leer_texto("Username: ")
        password = leer_texto("Password: ")

        usuarios = crud_usuario.listar_todos()

        for u in usuarios:
            if u.username == username and u.password_hash == password:
                print(f"\nBienvenido {u.nombre}\n")
                return u

        print("Credenciales incorrectas.\n")


# Menú Apuesta


def menu_apuestas(usuario_id: UUID) -> None:
    while True:
        print("\n--- Apuestas ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for c in crud_apuesta.listar_todos():
                print(f"  {c.id_apuesta} | {c.monto_apostado} | {c.estado}")
        elif op == "2":
            monto_apostado = leer_float("Monto apostado: ")
            estado = leer_texto("Estado: ")
            if monto_apostado:
                try:
                    crud_apuesta.crear(
                        usuario_id, sorteo_id, monto_apostado, usuario_id
                    )
                    print("Apuesta creada.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Monto apostado obligatorio.")
        elif op == "3":
            id_apuesta = leer_uuid("ID apuesta a actualizar: ")
            if not id_apuesta:
                print("ID inválido.")
                continue
            c = crud_apuesta.obtener_por_id(id_apuesta)
            if not c:
                print("No existe esa apuesta.")
                continue
            monto_apostado = leer_float(
                f"Nuevo monto apostado (actual: {c.monto_apostado}): "
            )
            estado = leer_texto(f"Nuevo estado (actual: {c.estado}): ")
            crud_apuesta.actualizar(
                id_apuesta,
                usuario_id,
                monto_apostado=monto_apostado,
                estado=estado if estado else c.estado,
            )
            print("Actualizado.")
        elif op == "4":
            id_apuesta = leer_uuid("ID apuesta a eliminar: ")
            if id_apuesta and crud_apuesta.eliminar(id_apuesta):
                print("Eliminada.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


# Menú Bingo
def menu_bingos(usuario_id: UUID) -> None:
    while True:
        print("\n--- Bingos ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")
        if op == "0":
            return
        if op == "1":
            for c in crud_bingo.listar_todos():
                print(
                    f"  {c.id_bingo} | {c.aciertos} | {c.carton_json} | {c.costo_entrada} | {c.recompensa}"
                )
        elif op == "2":
            aciertos = leer_int("Aciertos: ")
            costo_entrada = leer_float("Costo entrada: ")
            recompensa = leer_float("Recompensa: ")
            if costo_entrada:
                try:
                    crud_bingo.crear(costo, recompensa)
                    print("Bingo creado.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Costo de entrada obligatorio.")
        elif op == "3":
            id_bingo = leer_uuid("ID bingo a actualizar: ")
            if not id_bingo:
                print("ID inválido.")
                continue
            c = crud_bingo.obtener_por_id(id_bingo)
            if not c:
                print("No existe ese bingo.")
                continue
            costo_entrada = leer_float(
                f"Nuevo costo entrada (actual: {c.costo_entrada}): "
            )
            aciertos = leer_int(f"Nuevo aciertos (actual: {c.aciertos}): ")
            recompensa = leer_float(f"Nueva recompensa (actual: {c.recompensa}): ")

            crud_bingo.actualizar(
                id_bingo,
                aciertos=aciertos if aciertos else c.aciertos,
                costo_entrada=costo_entrada if costo_entrada else c.costo_entrada,
                recompensa=recompensa if recompensa else c.recompensa,
            )
            print("Actualizado.")
        elif op == "4":
            id_bingo = leer_uuid("ID bingo a eliminar: ")
            if id_bingo and crud_bingo.eliminar(id_bingo):
                print("Eliminado.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


# Menú Sorteo


def menu_sorteos(usuario_id: uuid.UUID) -> None:
    while True:
        print("\n--- Sorteos ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")

        if op == "0":
            return

        if op == "1":
            for s in sorteo_crud.listar_todos():
                juego = "-"
                if s.id_bingo:
                    juego = "Bingo"
                elif s.id_ruleta:
                    juego = "Ruleta"
                elif s.id_loteria:
                    juego = "Lotería"

                print(f"  {s.id_sorteo} | Fecha: {s.fecha_sorteo} | Juego: {juego}")

        elif op == "2":
            fecha = leer_fecha("Fecha sorteo (YYYY-MM-DD HH:MM): ")
            if fecha:
                try:
                    sorteo_crud.programar_sorteo(fecha_evento=fecha)
                    print("Sorteo creado.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("La fecha es obligatoria.")

        elif op == "3":
            id_s = leer_uuid("ID sorteo a actualizar: ")
            if not id_s:
                print("ID inválido.")
                continue

            s = sorteo_crud.obtener_por_id(id_s)
            if not s:
                print("No existe ese sorteo.")
                continue

            nueva_f = leer_fecha(f"Nueva fecha (actual: {s.fecha_sorteo}): ")
            sorteo_crud.actualizar(
                id_sorteo=id_s, fecha_sorteo=nueva_f if nueva_f else s.fecha_sorteo
            )
            print("Actualizado.")

        elif op == "4":
            id_s = leer_uuid("ID sorteo a eliminar: ")
            if id_s and sorteo_crud.eliminar(id_s):
                print("Eliminado.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


# Menú ruleta
def menu_ruleta():
    while True:
        print("\n--- Ruleta ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")

        op = leer_texto("Opción: ")

        if op == "0":
            return

        elif op == "1":
            ruletas = crud_ruleta.listar_todos()
            if not ruletas:
                print("No hay ruletas.")
            for r in ruletas:
                print(
                    f"{r.id_ruleta} | elección={r.eleccion_usuario} | costo={r.costo_entrada} | recompensa={r.recompensa}"
                )

        elif op == "2":
            try:
                eleccion = leer_texto("Elección (rojo/negro/etc): ")
                costo = leer_float("Costo entrada: ")
                recompensa = leer_float("Recompensa: ")

                r = crud_ruleta.crear(eleccion, costo, recompensa)
                print(f"Ruleta creada: {r.id_ruleta}")
            except Exception as e:
                print("Error:", e)

        elif op == "3":
            id_r = leer_uuid("ID de la ruleta: ")
            if not id_r:
                print("ID inválido")
                continue

            r = crud_ruleta.obtener_por_id(id_r)
            if not r:
                print("No existe esa ruleta.")
                continue

            print("Deja vacío para mantener valor actual")

            nueva_eleccion = (
                leer_texto(f"Elección ({r.eleccion_usuario}): ") or r.eleccion_usuario
            )

            nuevo_costo = leer_float(f"Costo ({r.costo_entrada}): ")
            if nuevo_costo <= 0:
                nuevo_costo = r.costo_entrada

            nueva_recompensa = leer_float(f"Recompensa ({r.recompensa}): ")
            if nueva_recompensa <= 0:
                nueva_recompensa = r.recompensa

            actualizado = crud_ruleta.actualizar(
                id_r,
                eleccion_usuario=nueva_eleccion,
                costo_entrada=nuevo_costo,
                recompensa=nueva_recompensa,
            )

            print("Actualizado." if actualizado else "Error al actualizar.")

        elif op == "4":
            id_r = leer_uuid("ID de la ruleta: ")
            if id_r and crud_ruleta.eliminar(id_r):
                print("Eliminada.")
            else:
                print("No se pudo eliminar.")


# Menú Loteria


def menu_loterias(usuario_id: UUID) -> None:
    while True:
        print("\n--- Loterías ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")

        if op == "0":
            return

        if op == "1":
            loterias = obtener_loterias()
            if not loterias:
                print("No hay loterías registradas.")
            else:
                for l in loterias:
                    print(
                        f"  {l.id_loteria} | Número: {l.numero_jugado} | Costo: ${l.costo_entrada:,.2f} | Premio: ${l.recompensa:,.2f}"
                    )

        elif op == "2":
            numero = leer_texto("Número de 4 dígitos: ")
            try:
                costo = float(leer_texto("Costo de entrada: $"))
                premio = float(leer_texto("Recompensa: $"))
                crear_loteria(numero, costo, premio)
                print("Lotería creada.")
            except ValueError as e:
                print("Error:", e)
            except Exception as e:
                print("Error inesperado:", e)

        elif op == "3":
            id_lot = leer_uuid("ID lotería a actualizar: ")
            if not id_lot:
                print("ID inválido.")
                continue

            l = obtener_loteria(id_lot)
            if not l:
                print("No existe esa lotería.")
                continue

            print("Deja en blanco los campos que no deseas actualizar.")

            numero = leer_texto(f"Nuevo número (actual: {l.numero_jugado}): ")
            costo = leer_texto(f"Nuevo costo (actual: ${l.costo_entrada:,.2f}): ")
            premio = leer_texto(f"Nueva recompensa (actual: ${l.recompensa:,.2f}): ")

            kwargs = {}
            if numero:
                kwargs["numero_jugado"] = numero
            if costo:
                try:
                    kwargs["costo_entrada"] = float(costo)
                except ValueError:
                    print("Costo inválido, no se actualizará.")
            if premio:
                try:
                    kwargs["recompensa"] = float(premio)
                except ValueError:
                    print("Recompensa inválida, no se actualizará.")

            if kwargs:
                try:
                    actualizar_loteria(id_lot, **kwargs)
                    print("Lotería actualizada.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("No se realizaron cambios.")

        elif op == "4":
            id_lot = leer_uuid("ID lotería a eliminar: ")
            if not id_lot:
                print("ID inválido.")
                continue

            try:
                if eliminar_loteria(id_lot):
                    print("Lotería eliminada.")
                else:
                    print("No se pudo eliminar (ID no existe).")
            except ValueError as e:
                print("Error:", e)


# Menú Metodo pago


def menu_metodos_pago(usuario_id: uuid.UUID) -> None:
    while True:
        print("\n--- Métodos de Pago ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")

        if op == "0":
            return

        if op == "1":
            metodos = metodo_pago_crud.listar_metodos_usuario(usuario_id)
            if not metodos:
                print("No tienes métodos registrados.")
            for m in metodos:
                print(
                    f"  {m.id_metodo_pago} | {m.tipo_metodo} | Titular: {m.nombre_titular}"
                )

        elif op == "2":
            tipo = leer_texto("Tipo (Nequi/Visa/Efectivo): ")
            titular = leer_texto("Nombre del titular: ")
            id_dueno = leer_uuid("ID del Usuario dueño: ")

            if tipo and titular and id_dueno:
                try:
                    metodo_pago_crud.registrar_metodo_pago(
                        tipo=tipo,
                        titular=titular,
                        id_dueno=id_dueno,
                        id_admin=usuario_id,
                    )
                    print("Método de pago creado.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Tipo, Titular e ID de dueño son obligatorios.")

        elif op == "3":
            id_m = leer_uuid("ID método a actualizar: ")
            if not id_m:
                print("ID inválido.")
                continue

            m = metodo_pago_crud.obtener_por_id(id_m)
            if not m:
                print("No existe ese método de pago.")
                continue

            nuevo_tp = (
                leer_texto(f"Nuevo tipo (actual: {m.tipo_metodo}): ") or m.tipo_metodo
            )
            nuevo_tt = (
                leer_texto(f"Nuevo titular (actual: {m.nombre_titular}): ")
                or m.nombre_titular
            )

            metodo_pago_crud.actualizar_metodo(
                id_metodo=id_m,
                nuevo_tipo=nuevo_tp,
                nuevo_titular=nuevo_tt,
                id_admin=usuario_id,
            )
            print("Actualizado.")

        elif op == "4":
            id_m = leer_uuid("ID método a eliminar: ")
            if id_m and metodo_pago_crud.eliminar(id_m):
                print("Eliminado.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


# Menú Transaccion


def menu_transacciones():
    while True:
        print("\n--- Transacciones ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")

        op = leer_texto("Opción: ")

        if op == "0":
            return

        elif op == "1":
            transacciones = crud_transaccion.listar_todos()
            if not transacciones:
                print("No hay transacciones.")
            for t in transacciones:
                print(
                    f"{t.id_transaccion} | tipo={t.tipo} | monto={t.monto} | billetera={t.id_billetera}"
                )

        elif op == "2":
            try:
                tipo = leer_texto("Tipo (ingreso/retiro): ")
                monto = leer_float("Monto: ")
                id_billetera = leer_uuid("ID billetera: ")
                id_metodo = leer_uuid("ID método pago: ")

                t = crud_transaccion.crear(
                    tipo,
                    monto,
                    id_billetera,
                    id_metodo,
                )
                print(f"Transacción creada: {t.id_transaccion}")
            except Exception as e:
                print("Error:", e)

        elif op == "3":
            id_t = leer_uuid("ID de la transacción: ")
            if not id_t:
                print("ID inválido")
                continue

            t = crud_transaccion.obtener_por_id(id_t)
            if not t:
                print("No existe esa transacción.")
                continue

            print("Deja vacío para mantener valor actual")

            nuevo_tipo = leer_texto(f"Tipo ({t.tipo}): ") or t.tipo

            nuevo_monto = leer_float(f"Monto ({t.monto}): ")
            if nuevo_monto <= 0:
                nuevo_monto = t.monto

            actualizada = crud_transaccion.actualizar(
                id_t,
                tipo=nuevo_tipo,
                monto=nuevo_monto,
            )

            print("Actualizada." if actualizada else "Error al actualizar.")

        elif op == "4":
            id_t = leer_uuid("ID de la transacción: ")
            if id_t and crud_transaccion.eliminar(id_t):
                print("Eliminada.")
            else:
                print("No se pudo eliminar.")


# Menú billetera


def menu_billeteras(usuario_id: UUID) -> None:
    while True:
        print("\n--- Billeteras ---")
        print(
            "1. Listar  2. Crear  3. Recargar  4. Consultar saldo  5. Eliminar  0. Volver"
        )
        op = leer_texto("Opción: ")

        if op == "0":
            return

        if op == "1":
            billeteras = billetera_crud.obtener_todas()
            if not billeteras:
                print("No hay billeteras registradas.")
            else:
                for b in billeteras:
                    print(
                        f"  {b.id_billetera} | Usuario: {b.id_usuario} | Saldo: ${b.saldo:,.2f}"
                    )

        elif op == "2":
            id_usuario = leer_uuid("ID del usuario: ")
            if not id_usuario:
                print("ID inválido.")
                continue
            try:
                billetera_crud.crear(id_usuario, usuario_id)
                print("Billetera creada.")
            except Exception as e:
                print("Error:", e)

        elif op == "3":
            id_billetera = leer_uuid("ID billetera a recargar: ")
            if not id_billetera:
                print("ID inválido.")
                continue
            try:
                monto = float(leer_texto("Monto a recargar: $"))
                billetera_crud.recargar_saldo(id_billetera, monto, usuario_id)
                print("Saldo recargado.")
            except Exception as e:
                print("Error:", e)

        elif op == "4":
            id_billetera = leer_uuid("ID billetera a consultar: ")
            if not id_billetera:
                print("ID inválido.")
                continue
            try:
                saldo = billetera_crud.consultar_saldo(id_billetera)
                print(f"Saldo actual: ${saldo:,.2f}")
            except Exception as e:
                print("Error:", e)

        elif op == "5":
            id_billetera = leer_uuid("ID billetera a eliminar: ")
            if id_billetera and billetera_crud.eliminar(id_billetera):
                print("Billetera eliminada.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


def main():
    usuario = ingresar_o_crear_usuario()

    if not usuario:
        print("No se pudo iniciar sesión.")
        return

    while True:
        print("\n========== Menú principal ==========")
        print("1. Apuestas")
        print("2. Bingo")
        print("3. Ruleta")
        print("4. Loteria")
        print("5. Sorteos")
        print("6. Billetera")
        print("7. Métodos de pago")
        print("8. Transacciones")
        print("0. Salir")

        op = leer_texto("Opción: ")

        if op == "0":
            print(f"Hasta luego {usuario.username}")
            break

        elif op == "1":
            menu_apuestas(usuario.id_usuario)

        elif op == "2":
            menu_bingos()

        elif op == "3":
            menu_ruleta()

        elif op == "4":
            menu_loterias()

        elif op == "5":
            menu_sorteos()

        elif op == "6":
            menu_billeteras()

        elif op == "7":
            menu_metodos_pago()

        elif op == "8":
            menu_transacciones()

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
