import threading
import copy
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# 1. SINGLETON: Configuración de Reglas centralizada
class ConfiguracionReglas:
    _instancia = None
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConfiguracionReglas, cls).__new__(cls)
            cls._instancia.hora_limite_prioridad = 18
            cls._instancia.ventana_canc_estudiante = timedelta(hours=2)
            cls._instancia.ventana_canc_capitan = timedelta(hours=24)
            cls._instancia.limite_no_shows = 3
            cls._instancia.dias_suspension = timedelta(days=7)
        return cls._instancia

# ENTIDADES DEL MODELO DE DOMINIO
class Cancha:
    def __init__(self, id_cancha):
        self.id_cancha = id_cancha

class Solicitante:
    def __init__(self, id_solicitante, tipo):
        self.id_solicitante = id_solicitante
        self.tipo = tipo
        self.historial_no_shows = []  # CORRECCIÓN: Lista para guardar fechas de no-shows
        self.fecha_suspension_fin = None

    def registrar_no_show(self, fecha_actual: datetime):
        self.historial_no_shows.append(fecha_actual)
        # CORRECCIÓN: Contar solo los no-shows del mismo mes calendario y año
        no_shows_mes = sum(
            1 for f in self.historial_no_shows 
            if f.year == fecha_actual.year and f.month == fecha_actual.month
        )
        if no_shows_mes >= ConfiguracionReglas().limite_no_shows:
            self.fecha_suspension_fin = fecha_actual + ConfiguracionReglas().dias_suspension

    def esta_suspendido(self, fecha_actual: datetime) -> bool:
        if self.fecha_suspension_fin and fecha_actual < self.fecha_suspension_fin:
            return True
        return False

# 2. STRATEGY (Regla de Prioridad)
class ReglaPrioridad(ABC):
    @abstractmethod
    def tiene_prioridad(self, solicitante: Solicitante) -> bool: pass

class PrioridadEquiposOficiales(ReglaPrioridad):
    def tiene_prioridad(self, solicitante: Solicitante) -> bool:
        return solicitante.tipo == "Capitan"

class PrioridadGeneral(ReglaPrioridad):
    def tiene_prioridad(self, solicitante: Solicitante) -> bool:
        return True

# 3. STRATEGY (Políticas de cancelación)
class PoliticaCancelacion(ABC):
    @abstractmethod
    def calcular_estado(self, fecha_reserva: datetime, fecha_cancelacion: datetime) -> str: pass

class CancelacionEstudiante(PoliticaCancelacion):
    def calcular_estado(self, fecha_reserva, fecha_cancelacion):
        if fecha_reserva - fecha_cancelacion < ConfiguracionReglas().ventana_canc_estudiante:
            return "NO-SHOW"
        return "CANCELADA"

class CancelacionCapitan(PoliticaCancelacion):
    def calcular_estado(self, fecha_reserva, fecha_cancelacion):
        if fecha_reserva - fecha_cancelacion < ConfiguracionReglas().ventana_canc_capitan:
            return "NO-SHOW"
        return "CANCELADA"

class CancelacionAdmin(PoliticaCancelacion):
    def calcular_estado(self, fecha_reserva, fecha_cancelacion):
        return "ANULADA"

# ENTIDAD PRINCIPAL
class Reserva:
    def __init__(self, cancha, fecha_hora, solicitante, sede_nombre, politica_canc):
        self.cancha = cancha
        self.fecha_hora = fecha_hora
        self.solicitante = solicitante
        self.sede_nombre = sede_nombre
        self.politica_canc = politica_canc
        self.estado = "CONFIRMADA"

    def cancelar(self, fecha_cancelacion: datetime):
        self.estado = self.politica_canc.calcular_estado(self.fecha_hora, fecha_cancelacion)
        if self.estado == "NO-SHOW":
            self.solicitante.registrar_no_show(fecha_cancelacion)

# 4. FACTORY METHOD
class ReservaFactory(ABC):
    @abstractmethod
    def crear_reserva(self, cancha, f_hora, sol, sede) -> Reserva: pass

class FabricaReservaEstudiante(ReservaFactory):
    def crear_reserva(self, cancha, f_hora, sol, sede):
        return Reserva(cancha, f_hora, sol, sede, CancelacionEstudiante())

class FabricaReservaCapitan(ReservaFactory):
    def crear_reserva(self, cancha, f_hora, sol, sede):
        return Reserva(cancha, f_hora, sol, sede, CancelacionCapitan())

# 5. ABSTRACT FACTORY (Sedes)
class ValidadorHorario(ABC):
    @abstractmethod
    def es_valido(self, hora: int) -> bool: pass

class Notificador(ABC):
    @abstractmethod
    def notificar(self, mensaje: str): pass

class SedeNorteFactory:
    def validador(self): return type('VN', (ValidadorHorario,), {'es_valido': lambda self, h: 6 <= h < 22})()
    def notificador(self): return type('NN', (Notificador,), {'notificar': lambda self, msg: print(f"[Email Norte] {msg}")})()

class SedeSurFactory:
    def validador(self): return type('VS', (ValidadorHorario,), {'es_valido': lambda self, h: 7 <= h < 23})()
    def notificador(self): return type('NS', (Notificador,), {'notificar': lambda self, msg: print(f"[SMS Sur] {msg}")})()

# Entidad Reserva Recurrente (Concepto de Dominio)
class ReservaRecurrente:
    def __init__(self):
        self.cancha = None
        self.fecha_inicio = None
        self.solicitante = None
        self.sede_nombre = None
        self.semanas = 0
        self.equipo = None
        self.notas = None
        self.reservas = [] # Agrupa las reservas individuales

# 6. BUILDER (Recurrente)
class BuilderReservaRecurrente:
    def __init__(self): 
        self.reserva_recurrente = ReservaRecurrente()
        
    def set_obligatorios(self, c, f_inicio, s, sede): 
        self.reserva_recurrente.cancha = c
        self.reserva_recurrente.fecha_inicio = f_inicio
        self.reserva_recurrente.solicitante = s
        self.reserva_recurrente.sede_nombre = sede
        return self
        
    def set_semanas(self, semanas): 
        if not (2 <= semanas <= 8):
            raise ValueError("Las semanas deben estar entre 2 y 8")
        self.reserva_recurrente.semanas = semanas
        return self
        
    def set_equipo(self, eq): 
        self.reserva_recurrente.equipo = eq
        return self
        
    def set_notas(self, notas):
        self.reserva_recurrente.notas = notas
        return self
        
    def build(self): 
        if self.reserva_recurrente.semanas < 2:
            raise ValueError("Faltan semanas por configurar.")
        return self.reserva_recurrente

# 7. PROTOTYPE (Bloqueos)
class Bloqueo:
    def __init__(self, motivo, franja, equipo):
        self.motivo, self.franja, self.equipo = motivo, franja, equipo
    def clone(self, cancha, fecha):
        clon = copy.copy(self)
        clon.cancha, clon.fecha = cancha, fecha
        return clon

# 8. FACADE Y CONCURRENCIA
class ReservaFacade:
    def __init__(self):
        self.sedes = {"Norte": SedeNorteFactory(), "Sur": SedeSurFactory()}
        self.reservas = []
        self.bloqueos = []
        self.lock = threading.Lock()

    # Operación 1: Reservar Normal
    def reservar(self, cancha: Cancha, fecha_hora: datetime, solicitante: Solicitante, id_sede: str, fecha_actual: datetime):
        sede = self.sedes[id_sede]
        if solicitante.esta_suspendido(fecha_actual):
            sede.notificador().notificar(f"Rechazo: {solicitante.id_solicitante} suspendido.")
            return False

        if not sede.validador().es_valido(fecha_hora.hour):
            sede.notificador().notificar("Fuera de horario permitido en la sede.")
            return False

        regla = PrioridadEquiposOficiales() if fecha_hora.hour < ConfiguracionReglas().hora_limite_prioridad else PrioridadGeneral()
        if not regla.tiene_prioridad(solicitante):
            sede.notificador().notificar("Rechazo: Horario requiere prioridad de Capitán.")
            return False

        with self.lock:
            for r in self.reservas:
                if r.cancha.id_cancha == cancha.id_cancha and r.fecha_hora == fecha_hora and r.estado == "CONFIRMADA":
                    sede.notificador().notificar("Rechazo: Cancha ya ocupada.")
                    return False
            
            fact = FabricaReservaEstudiante() if solicitante.tipo == "Estudiante" else FabricaReservaCapitan()
            reserva = fact.crear_reserva(cancha, fecha_hora, solicitante, id_sede)
            self.reservas.append(reserva)
            sede.notificador().notificar(f"Éxito: Reserva confirmada para {solicitante.id_solicitante}.")
            return True

    # Operación 2: Reservar Recurrente (Todo o nada)
    def reservar_recurrente(self, builder: BuilderReservaRecurrente, fecha_actual: datetime):
        req = builder.build()
        sede = self.sedes[req.sede_nombre]
        
        if req.solicitante.esta_suspendido(fecha_actual):
            sede.notificador().notificar(f"Rechazo: {req.solicitante.id_solicitante} suspendido.")
            return False

        fechas_a_reservar = [req.fecha_inicio + timedelta(days=7*i) for i in range(req.semanas)]

        with self.lock:
            # 1. Verificar disponibilidad de TODAS las semanas primero
            for i, f in enumerate(fechas_a_reservar):
                for r in self.reservas:
                    if r.cancha.id_cancha == req.cancha.id_cancha and r.fecha_hora == f and r.estado == "CONFIRMADA":
                        sede.notificador().notificar(f"Rechazo Recurrente: Conflicto en la semana {i+1} ({f}). Operación cancelada (Todo o Nada).")
                        return False
            
            # 2. Si todo está libre, instanciar reservas
            fact = FabricaReservaCapitan()
            for f in fechas_a_reservar:
                res = fact.crear_reserva(req.cancha, f, req.solicitante, req.sede_nombre)
                req.reservas.append(res)
                self.reservas.append(res)
                
            sede.notificador().notificar(f"Éxito: Reserva recurrente de {req.semanas} semanas confirmada.")
            return True

    # Operación 3: Cancelar
    def cancelar(self, reserva: Reserva, fecha_cancelacion: datetime, es_admin: bool = False):
        if es_admin:
            reserva.politica_canc = CancelacionAdmin() # Aplica Strategy en runtime
        reserva.cancelar(fecha_cancelacion)
        print(f"[Sistema] Reserva cancelada. Estado final: {reserva.estado}")

    # Operación 4: Bloquear
    def bloquear(self, plantilla: Bloqueo, canchas: list, fechas: list, fecha_actual: datetime):
        sede = self.sedes["Norte"] # Por simplicidad asumimos canal unificado o buscamos la sede
        with self.lock:
            for c in canchas:
                for f in fechas:
                    clon = plantilla.clone(c, f)
                    self.bloqueos.append(clon)
                    
                    # Buscar y anular reservas afectadas
                    for r in self.reservas:
                        if r.cancha.id_cancha == c.id_cancha and r.fecha_hora == f and r.estado == "CONFIRMADA":
                            self.cancelar(r, fecha_actual, es_admin=True)
                            self.sedes[r.sede_nombre].notificador().notificar(f"Aviso: Su reserva el {f} ha sido ANULADA por bloqueo administrativo.")