class Estudiante:
    def __init__(self, nombre):
        self.nombre = nombre

class EquipoOficial:
    def __init__(self, nombre):
        self.nombre = nombre

class ReservaRegular:
    def __init__(self, cancha, fecha, Hora_inicio, Hora_fin, Solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.Hora_inicio = Hora_inicio
        self.Hora_fin = Hora_fin
        self.solicitante = Solicitante

    def confirmar(self):
        return "Reserva confirmada para: " + self.solicitante.nombre

class ReservaPrioridad:
    def __init__(self, cancha, fecha, Hora_inicio, Hora_fin, Solicitante):
        self.cancha = cancha
        self.fecha = fecha
        self.Hora_inicio = Hora_inicio
        self.Hora_fin = Hora_fin
        self.solicitante = Solicitante

    def confirmar(self):
        return "Reserva con prioridad confirmada para: " + self.solicitante.nombre


class CreadorReserva():
    def crear_reserva(self, cancha, fecha, Hora_inicio, Hora_fin, solicitante):
        raise NotImplementedError

class creadorDeReservaRegular(CreadorReserva):
    def crear_reserva(self, cancha, fecha, Hora_inicio, Hora_fin, solicitante):
        return ReservaRegular(
            cancha,
            fecha,
            Hora_inicio,
            Hora_fin,
            solicitante
            )

class creadorDeReservaPrioridad(CreadorReserva):
    def crear_reserva(self, cancha, fecha, Hora_inicio, Hora_fin, solicitante):
        return ReservaPrioridad(
            cancha,
            fecha,
            Hora_inicio,
            Hora_fin,
            solicitante
            )

class fabricaDeReservas():
    @staticmethod
    def elegirCreador(solicitante):
        if isinstance(solicitante, Estudiante):
            return creadorDeReservaRegular()
        elif isinstance(solicitante, EquipoOficial):
            return creadorDeReservaPrioridad()
            

def reservar_desde_web(cancha, fecha, Hora_inicio, Hora_fin, solicitante):
    creador = fabricaDeReservas.elegirCreador(solicitante)
    reserva = creador.crear_reserva(
        cancha,
        fecha,
        Hora_inicio,
        Hora_fin,
        solicitante
    )
    return reserva


def main():
    reserva1 = reservar_desde_web(
        'cancha de Futbol',
        '2026-09-17',
        '18:00',
        '20:00',
        Estudiante('Carlos')
        )
       
    reserva2 = reservar_desde_web( 
        'cancha de Futbol',
        '2026-09-17',
        '18:00',
        '20:00',
        EquipoOficial('Carlos_Capitan')
    )

    print(reserva1.confirmar())
    print(reserva2.confirmar())

if __name__ =="__main__":
    main()