import sys
from typing import Optional
from src.entities.usuario import Usuario
from typing import cast
from uuid import UUID
from datetime import datetime
from src.database.config import engine, Base

sys.path.insert(0, ".")

from src.crud import apuesta_crud as crud_apuesta
from src.crud import bingo_crud as crud_bingo
from src.crud import sorteo_crud as crud_sorteo
from src.crud import usuario_crud as crud_usuario
from src.crud import ruleta_crud as crud_ruleta
from src.crud import transaccion_crud as crud_transaccion
from src.crud import metodo_pago_crud as crud_metodo_pago
from src.crud import loteria_crud as crud_loteria
from src.crud import billetera_crud as crud_billetera


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


def ingresar_o_crear_usuario() -> Optional[Usuario]:

    if len(crud_usuario.listar_todos()) == 0:
        print("\n--- No hay usuarios registrados ---")
        print("Por favor, cree la cuenta de administrador:\n")

        nombre = leer_texto("Nombre: ")
        username = leer_texto("Username: ")
        email = leer_texto("Email: ")
        password = leer_texto("Password: ")

        try:
            crud_usuario.crear_usuario(
                nombre=nombre, username=username, password=password, email=email
            )
            print("Usuario creado con éxito. Ahora inicie sesión.\n")
        except Exception as e:
            print(f"Error al crear usuario: {e}")
            return None

    while True:
        print("--- Inicio de sesión ---")
        user_input = leer_texto("Username: ")
        pass_input = leer_texto("Password: ")

        usuarios = crud_usuario.listar_todos()

        for u in usuarios:

            if (
                getattr(u, "username") == user_input
                and getattr(u, "password_hash") == pass_input
            ):
                print(f"\n¡Bienvenido de nuevo, {u.nombre}!")
                return u

        print("Credenciales incorrectas. Intente de nuevo.\n")


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
            id_sorteo = leer_uuid("Ingrese el ID del sorteo: ")
            monto_apostado = leer_float("Monto apostado: ")
            if id_sorteo and monto_apostado:
                try:
                    crud_apuesta.crear(
                        id_usuario=usuario_id,
                        id_sorteo=id_sorteo,
                        monto=monto_apostado,
                        id_usuario_creacion=usuario_id,
                    )
                    print("Apuesta creada.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Error: El ID del sorteo y el monto son obligatorios.")
        elif op == "3":
            id_apuesta = leer_uuid("ID apuesta a actualizar: ")
            if not id_apuesta:
                print("ID inválido.")
                continue

            c = crud_apuesta.obtener_por_id(id_apuesta)
            if not c:
                print("No existe esa apuesta.")
                continue

            monto_apostado = leer_float(f"Nuevo monto (actual: {c.monto_apostado}): ")
            nuevo_estado = leer_texto(
                f"Nuevo estado (actual: {c.estado}):GANADA/PERDIDA/PENDIENTE "
            ).upper()
            datos_actualizar = {}
            if monto_apostado is not None:
                datos_actualizar["monto_apostado"] = monto_apostado
            if nuevo_estado:
                datos_actualizar["estado"] = nuevo_estado
            crud_apuesta.actualizar(id_apuesta, usuario_id, **datos_actualizar)
            print("Actualizado.")
        elif op == "4":
            id_apuesta = leer_uuid("ID apuesta a eliminar: ")
            if id_apuesta and crud_apuesta.eliminar(id_apuesta):
                print("Eliminada.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


# Menú Loteria


def menu_loterias(usuario_id: UUID) -> None:
    while True:
        print("\n--- Loterías ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")

        if op == "0":
            return

        elif op == "1":
            loterias = crud_loteria.obtener_loterias()
            if not loterias:
                print("No hay loterías registradas.")
            else:
                for l in loterias:
                    print(
                        f"  {l.id_loteria} | Número: {l.numero_jugado} | "
                        f"Costo: ${l.costo_entrada:,.2f} | Premio: ${l.recompensa:,.2f}"
                    )

        elif op == "2":
            numero = leer_texto("Número de 4 dígitos: ")
            costo = leer_float("Costo de entrada: $")
            premio = leer_float("Recompensa: $")
            try:
                crud_loteria.crear_loteria(
                    numero_jugado=numero, costo_entrada=costo, recompensa=premio
                )
                print("Lotería creada.")
            except Exception as e:
                print("Error:", e)

        elif op == "3":
            id_lot = leer_uuid("ID lotería a actualizar: ")
            if not id_lot:
                print("ID inválido.")
                continue

            l = crud_loteria.obtener_loteria(id_lot)
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
                    crud_loteria.actualizar_loteria(id_lot, **kwargs)
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
                if crud_loteria.eliminar_loteria(id_lot):
                    print("Lotería eliminada.")
                else:
                    print("No se pudo eliminar (ID no existe).")
            except Exception as e:
                print("Error:", e)


# Menú Bingo


def menu_bingos(usuario_id: UUID) -> None:
    while True:
        print("\n--- Bingos ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")

        if op == "0":
            return

        elif op == "1":
            bingos = crud_bingo.listar_todos()
            if not bingos:
                print("No hay bingos registrados.")
            else:
                for c in bingos:
                    print(
                        f"  {c.id_bingo} | Aciertos: {c.aciertos} | "
                        f"Cartón: {c.carton_json} | "
                        f"Costo: ${c.costo_entrada:,.2f} | "
                        f"Recompensa: ${c.recompensa:,.2f}"
                    )

        elif op == "2":
            costo_entrada = leer_float("Costo entrada: $")
            recompensa = leer_float("Recompensa: $")

            if costo_entrada:
                try:
                    crud_bingo.crear(costo=costo_entrada, recompensa=recompensa)
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
            recompensa = leer_float(f"Nueva recompensa (actual: {c.recompensa}): ")

            kwargs = {}
            if costo_entrada:
                kwargs["costo_entrada"] = costo_entrada
            if recompensa:
                kwargs["recompensa"] = recompensa

            if kwargs:
                try:
                    crud_bingo.actualizar(id_bingo, **kwargs)
                    print("Bingo actualizado.")
                except Exception as e:
                    print("Error:", e)
            else:
                print("No se realizaron cambios.")

        elif op == "4":
            id_bingo = leer_uuid("ID bingo a eliminar: ")
            if not id_bingo:
                print("ID inválido.")
                continue

            if crud_bingo.eliminar(id_bingo):
                print("Eliminado.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


# Menú Sorteo


def leer_fecha(mensaje: str) -> Optional[datetime]:
    s = input(mensaje).strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d %H:%M")
    except ValueError:
        print("Formato inválido. Usa YYYY-MM-DD HH:MM")
        return None


def menu_sorteos(usuario_id: UUID) -> None:
    while True:
        print("\n--- Sorteos ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")

        if op == "0":
            return

        elif op == "1":
            for s in crud_sorteo.listar_todos():
                if s.id_bingo is not None:
                    juego = "Bingo"
                elif s.id_ruleta is not None:
                    juego = "Ruleta"
                elif s.id_loteria is not None:
                    juego = "Lotería"
                else:
                    juego = "-"

                print(f"  {s.id_sorteo} | Fecha: {s.fecha_sorteo} | Juego: {juego}")

        elif op == "2":
            fecha = leer_fecha("Fecha sorteo (YYYY-MM-DD HH:MM): ")
            if fecha:
                try:
                    crud_sorteo.programar_sorteo(fecha_evento=fecha)
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

            s = crud_sorteo.obtener_por_id(id_s)
            if not s:
                print("No existe ese sorteo.")
                continue

            nueva_f = leer_fecha(f"Nueva fecha (actual: {s.fecha_sorteo}): ")
            crud_sorteo.actualizar(
                id_sorteo=id_s, fecha_sorteo=nueva_f if nueva_f else s.fecha_sorteo
            )
            print("Actualizado.")

        elif op == "4":
            id_s = leer_uuid("ID sorteo a eliminar: ")
            if id_s and crud_sorteo.eliminar(id_s):
                print("Eliminado.")
            else:
                print("No se pudo eliminar.")


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
            entrada_eleccion = leer_texto(f"Elección ({r.eleccion_usuario}): ")
            entrada_costo = leer_float(f"Costo ({r.costo_entrada}): ")
            entrada_recompensa = leer_float(f"Recompensa ({r.recompensa}): ")
            datos_actualizar = {
                "eleccion_usuario": entrada_eleccion if entrada_eleccion else None,
                "costo_entrada": entrada_costo if entrada_costo > 0 else None,
                "recompensa": entrada_recompensa if entrada_recompensa > 0 else None,
            }
            actualizado = crud_ruleta.actualizar(id_r, **datos_actualizar)
            print("Actualizado." if actualizado else "Error al actualizar.")

        elif op == "4":
            id_r = leer_uuid("ID de la ruleta: ")
            if id_r and crud_ruleta.eliminar(id_r):
                print("Eliminada.")
            else:
                print("No se pudo eliminar.")


# Menú Metodo pago


def menu_metodos_pago(usuario_id: UUID) -> None:
    while True:
        print("\n--- Métodos de Pago ---")
        print("1. Listar  2. Crear  3. Actualizar  4. Eliminar  0. Volver")
        op = leer_texto("Opción: ")

        if op == "0":
            return

        if op == "1":
            metodos = crud_metodo_pago.listar_metodos_usuario(usuario_id)
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
                    crud_metodo_pago.registrar_metodo_pago(
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
            m = crud_metodo_pago.obtener_por_id(id_m)
            if not m:
                print("No existe ese método de pago.")
                continue
            nuevo_tp = leer_texto(f"Nuevo tipo (actual: {m.tipo_metodo}): ")
            nuevo_tt = leer_texto(f"Nuevo titular (actual: {m.nombre_titular}): ")
            crud_metodo_pago.actualizar_metodo(
                id_metodo=id_m,
                nuevo_tipo=nuevo_tp if nuevo_tp else None,
                nuevo_titular=nuevo_tt if nuevo_tt else None,
                id_admin=usuario_id,
            )
            print("Actualizado.")

        elif op == "4":
            id_m = leer_uuid("ID método a eliminar: ")
            if id_m and crud_metodo_pago.eliminar(id_m):
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
                tipo = leer_texto("Tipo (ingreso/retiro): ").upper()
                monto = leer_float("Monto: ")
                id_billetera = leer_uuid("ID billetera: ")
                id_metodo = leer_uuid("ID método pago: ")

                if tipo and monto > 0 and id_billetera and id_metodo:
                    t = crud_transaccion.crear(
                        tipo=tipo,
                        monto=monto,
                        id_billetera=id_billetera,
                        id_metodo_pago=id_metodo,
                    )
                    print(f"Transacción creada: {t.id_transaccion}")
                else:
                    print(
                        "Todos los campos son obligatorios y el monto debe ser mayor a 0."
                    )
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

            entrada_tipo = leer_texto(f"Nuevo tipo (actual: {t.tipo}): ")
            entrada_monto = leer_float(f"Nuevo monto (actual: {t.monto}): ")

            datos_actualizar = {}
            if entrada_tipo:
                datos_actualizar["tipo"] = entrada_tipo
            if entrada_monto > 0:
                datos_actualizar["monto"] = entrada_monto

            if datos_actualizar:
                actualizada = crud_transaccion.actualizar(id_t, **datos_actualizar)
                print("Actualizada." if actualizada else "Error al actualizar.")
            else:
                print("No se realizaron cambios.")

        elif op == "4":
            id_t = leer_uuid("ID de la transacción: ")
            if id_t and crud_transaccion.eliminar(id_t):
                print("Eliminada.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


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
            billeteras = crud_billetera.obtener_por_usuario(usuario_id)
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
                crud_billetera.crear(id_usuario, usuario_id)
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
                crud_billetera.recargar_saldo(id_billetera, monto, usuario_id)
                print("Saldo recargado.")
            except Exception as e:
                print("Error:", e)

        elif op == "4":
            id_billetera = leer_uuid("ID billetera a consultar: ")
            if not id_billetera:
                print("ID inválido.")
                continue
            try:
                saldo = crud_billetera.consultar_saldo(id_billetera)
                print(f"Saldo actual: ${saldo:,.2f}")
            except Exception as e:
                print("Error:", e)

        elif op == "5":
            id_billetera = leer_uuid("ID billetera a eliminar: ")
            if id_billetera and crud_billetera.eliminar(id_billetera):
                print("Billetera eliminada.")
            else:
                print("No se pudo eliminar (ID inválido o no existe).")


def main():
    Base.metadata.create_all(bind=engine)
    usuario = ingresar_o_crear_usuario()

    if not usuario:
        print("No se pudo iniciar sesión.")
        return

    uid = cast(UUID, usuario.id_usuario)

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
            menu_apuestas(uid)

        elif op == "2":
            menu_bingos(uid)

        elif op == "3":
            menu_ruleta()

        elif op == "4":
            menu_loterias(uid)

        elif op == "5":
            menu_sorteos(uid)

        elif op == "6":
            menu_billeteras(uid)

        elif op == "7":
            menu_metodos_pago(uid)

        elif op == "8":
            menu_transacciones()

        else:
            print("Opción no válida.")


if __name__ == "__main__":
    main()
