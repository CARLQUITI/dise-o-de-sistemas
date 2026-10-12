import threading
import time
from datetime import datetime, timedelta
from patrones import ReservaFacade, Solicitante, Cancha, BuilderReservaRecurrente, Bloqueo

def ejecutar_simulacion():
    print("=== INICIANDO SIMULACIÓN PSET 2 ===\n")
    facade = ReservaFacade()
    
    ahora = datetime(2026, 10, 15, 12, 0)
    cancha1 = Cancha("Cancha_Central")
    cancha2 = Cancha("Cancha_Secundaria")
    est1 = Solicitante("Juan_Estudiante", "Estudiante")
    cap1 = Solicitante("Messi_Capitan", "Capitan")

    print("--- 1. Reservas validadas por sede ---")
    facade.reservar(cancha1, datetime(2026, 10, 20, 19, 0), est1, "Norte", ahora)
    facade.reservar(cancha2, datetime(2026, 10, 20, 19, 0), cap1, "Sur", ahora)
    
    print("\n--- 2. Fuera de horario permitido ---")
    facade.reservar(cancha1, datetime(2026, 10, 21, 5, 0), est1, "Norte", ahora)

    print("\n--- 3. Reserva Recurrente (Todo o Nada) ---")
    builder = BuilderReservaRecurrente().set_obligatorios(cancha1, datetime(2026, 11, 1, 10, 0), cap1, "Sur").set_semanas(3).set_equipo("Balones")
    print("Intento exitoso:")
    facade.reservar_recurrente(builder, ahora)
    
    print("\nIntento con conflicto en semana 2:")
    # Ocupamos la semana 2 manualmente
    facade.reservar(cancha2, datetime(2026, 11, 8, 10, 0), est1, "Sur", ahora)
    builder_conflicto = BuilderReservaRecurrente().set_obligatorios(cancha2, datetime(2026, 11, 1, 10, 0), cap1, "Sur").set_semanas(3)
    facade.reservar_recurrente(builder_conflicto, ahora) # Fallará por la semana 2

    print("\n--- 4. Cancelaciones Múltiples (Strategy) ---")
    res_juan = [r for r in facade.reservas if r.solicitante.id_solicitante == "Juan_Estudiante"][0]
    res_messi = [r for r in facade.reservas if r.solicitante.id_solicitante == "Messi_Capitan" and r.cancha.id_cancha == "Cancha_Secundaria"][0]
    
    # 4a. Estudiante a tiempo (4h antes, límite 2h) -> CANCELADA
    facade.cancelar(res_juan, res_juan.fecha_hora - timedelta(hours=4))
    # 4b. Capitán tarde (10h antes, límite 24h) -> NO-SHOW
    facade.cancelar(res_messi, res_messi.fecha_hora - timedelta(hours=10))
    
    print("\n--- 5. Suspensión Automática por 3 No-shows en el mes ---")
    # Generamos 3 no-shows a Juan dentro de octubre 2026
    est1.registrar_no_show(datetime(2026, 10, 1))
    est1.registrar_no_show(datetime(2026, 10, 5))
    est1.registrar_no_show(datetime(2026, 10, 10))
    print(f"Suspendido Juan? {est1.esta_suspendido(ahora)}")
    facade.reservar(cancha1, datetime(2026, 10, 25, 19, 0), est1, "Norte", ahora)

    print("\n--- 6. Bloqueo Clonado (Prototype) y Anulación Administrativa ---")
    plantilla = Bloqueo("Mantenimiento", "10:00", "Ninguno")
    # Messi tiene reservas recurrentes el 1, 8 y 15 de Nov. Bloquearemos el 8.
    facade.bloquear(plantilla, [cancha1, cancha2], [datetime(2026, 11, 8, 10, 0)], ahora)

    print("\n--- 7. Concurrencia (Doble petición simultánea) ---")
    # Usamos Barrier para asegurar que ambos hilos intenten reservar al MISMO milisegundo exacto
    barrera = threading.Barrier(2)
    def intentar_reserva(nombre):
        temp_user = Solicitante(nombre, "Capitan")
        barrera.wait() # Ambos hilos se esperan aquí antes de atacar el Facade
        facade.reservar(cancha1, datetime(2026, 12, 1, 15, 0), temp_user, "Sur", ahora)

    t1 = threading.Thread(target=intentar_reserva, args=("Hilo_1",))
    t2 = threading.Thread(target=intentar_reserva, args=("Hilo_2",))
    t1.start(); t2.start()
    t1.join(); t2.join()

if __name__ == "__main__":
    ejecutar_simulacion()