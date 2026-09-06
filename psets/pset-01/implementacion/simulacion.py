#Estudiante1 -> realizará una reservación de la cancha, despues de las 6PM -> No tendra exito con la reservación.
#Capitan1 -> Realizara una reservacion de la cancha, antes de las 6PM -> Tendra exito con la reservacion.
#Estudiante2 ->tiene una reserva y quiere cancelarla con menos de 2 horas de anticipacion a la reserva
class comportamientoCliente:
    def cliente(self):
        raise NotImplementedError("Este metodo debe ser implementado")
class estudiante(comportamientoCliente):
    def cliente(self):
        print("Estudiante: ")
class capitan(comportamientoCliente):
    def cliente(self):
        print("Capitan: ")
    def cliente(self):
        print("administrador")

class comportamientoCrearReserva:
    def crearReserva(self):
        raise NotImplementedError("Este metodo debe ser implementado")
class MostrarHorario(comportamientoCrearReserva):
    def crearReserva(self):
        print("Mostrar Horario")
class verificarDisponibilidad(comportamientoCrearReserva):
    def crearReserva(self):
        print("Verificando disponibilidad")

class comportamientoPrioridad:
    def prioridad(self):
        raise NotImplementedError("Este metodo debe ser implementado")
class prioridadHora(comportamientoPrioridad):
    def prioridad(self):
        print("Verificando prioridad de la Hora")
class prioridadantes6Pm(comportamientoPrioridad):
    def prioridad(self):
        print("Aplica prioridad antes de las 6PM")
class prioridadDespues6PM(comportamientoPrioridad):
    def prioridad(self):
        print("No aplica prioridad despues de las 6PM")
class prioridadCapitan(comportamientoPrioridad):
    def prioridad(self):
        print("Prioridad de Capitan")
class prioridadNoCapitan(comportamientoPrioridad):
    def prioridad(self):
        print("No aplica prioridad de Capitan")

class comportamientoConfirmacion:
    def confirmacionReserva(self):
        raise NotImplementedError("Este metodo debe ser implementado")
class confirmacionExitosa(comportamientoConfirmacion):
    def confirmacionReserva(self):
        print("Reserva Confirmada Exitosamente")
class confirmacionFallida(comportamientoConfirmacion):
    def confirmacionReserva(self):
        print("La reserva no pudo ser confirmada, intente nuevamente")
    
class comportamientoCancelar:
    def cancelar(self):
        raise NotImplementedError("Este metodo debe ser implementado")
class comportamientoConReserva(comportamientoCancelar):
    def cancelar(self):
        print("Si existe reserva")
class comportamientoSinReserva(comportamientoCancelar):
    def cancelar(self):
        print("Debe tener almenos una reserva para cancelar. HAZ UNA RESERVA")
class cancelarAntes(comportamientoCancelar):
    def cancelar(self):
        print("NOSHOW")
class cancelarNormal(comportamientoCancelar):
    def cancelar(self):
        print("Cancelacion Normal")

class comportamientoGestion:
    def gestion(self):
        raise NotImplementedError("Este metodo no está implementado")
class gestionCanchas(comportamientoGestion):
    def gestion(self):
        print("Disponibilidad de canchas")
class gestionReservas(comportamientoGestion):
    def gestion(self):
        print("Reservas prioritarias")
class gestionMantenimiento(comportamientoGestion):
    def gestion(self):
        print("Mantenimiento de canchas")

class Reserva:
    def __init__(self, comportamientoCliente, comportamientoCrearReserva,comportamientoPrioridad, comportamientoConfirmacion):
        self.comportamientoCliente = comportamientoCliente
        self.comportamientoCrearReserva = comportamientoCrearReserva
        self.comportamientoPrioridad = comportamientoPrioridad
        self.comportamientoConfirmacion = comportamientoConfirmacion

    def mostrarcliente(self):
        self.comportamientoCliente.cliente()

    def CrearReserva(self):
        self.comportamientoCrearReserva.crearReserva()

    def mostrarPrioridad(self):
        self.comportamientoPrioridad.prioridad()

    def confirmacion(self):
        self.comportamientoConfirmacion.confirmacionReserva()

    def CancelarReserva(self):
        self.comportamientoCancelar.cancelar()

class Gestion:
    def __init__(self, comportamientoGestion):
        self.comportamientoGestion = comportamientoGestion

    def Administracion(self):
        for comportamiento in self.comportamientoGestion:
            comportamiento.gestion()

class CancelionReserva:
    def __init__(self, comportamientoCancelar):
        self.comportamientoCancelar = comportamientoCancelar

    def CancelarReservas(self):
        for cancelacion in self.comportamientoCancelar:
            cancelacion.cancelar()
#----------------------------------------------------------------------------------------------------
class estudianteNormal(Reserva):
    def __init__(self):
        Estudiante1 = estudiante()
        Reserva1 = verificarDisponibilidad()
        prioridad1 = prioridadDespues6PM()
        confirmacion1 = confirmacionFallida()
        super().__init__(Estudiante1,Reserva1,prioridad1, confirmacion1)
#----------------------------------------------------------------------------------------------------
class Capitan(Reserva):
    def __init__(self):
        capitan1 = capitan()
        Reserva2 = verificarDisponibilidad()
        prioridad3 = prioridadantes6Pm()
        confirmacion2 = confirmacionExitosa()
        super().__init__(capitan1, Reserva2,prioridad3, confirmacion2)
#----------------------------------------------------------------------------------------------------
class Administrador(Gestion):
    def __init__(self):
        Gestion1 = gestionCanchas()
        Gestion2 = gestionReservas()
        Gestion3 = gestionMantenimiento()
        gestiones = [Gestion1, Gestion2, Gestion3]

        super().__init__(gestiones)
#--------------------------------------------------------------------------------------------
class CancelarReservaEstudiante(CancelionReserva):
    def __init__(self):
        Cancelacion1 = comportamientoConReserva()
        cancelacion2 = cancelarAntes()
        cancelacionesTotales = [Cancelacion1, cancelacion2]
        super().__init__(cancelacionesTotales)
#--------------------------------------------------------------------------------------------
if __name__ == "__main__":
    print()
    print("-------------------------------------------------")
    print()
    Solicitud1 = estudianteNormal()
    Solicitud1.mostrarcliente()
    Solicitud1.CrearReserva()
    Solicitud1.mostrarPrioridad()
    Solicitud1.confirmacion()
    print()
    print("-------------------------------------------------")
    print()
#---------------------------------------    
    Solicitud2 = Capitan()
    Solicitud2.mostrarcliente()
    Solicitud2.CrearReserva()
    Solicitud2.mostrarPrioridad()
    Solicitud2.confirmacion()
    print()
    print("-------------------------------------------------")
    print()
#----------------------------------------  
    print("Administrador1:")
    Administracion1 = Administrador()
    Administracion1.Administracion()
    print()
    print("-------------------------------------------------")
    print()
#----------------------------------------
    print("Estudiante2: ")
    Cancelacion1 = CancelarReservaEstudiante()
    Cancelacion1.CancelarReservas()