#vehiculo ->mueva -> mover()

#auto -> mueve por carretera
#bote -> mueve por mar
#Avion -> mueve por cielo
class comportamientoVehiculo:
     def mover(self):
            raise NotImplementedError("Este metodo no esta implementado")
class Tierra(comportamientoVehiculo):
    def carretera(self):
         print("conduciendo por carretera")
class Agua(comportamientoVehiculo):
    def mar(self):
          print("Navegando por mar")
class Aire(comportamientoVehiculo):
     def cielo(self):
          print("Volando por cielo")

class Mover:
    def __init__(self, comportamientoVehiculo):
        self.comportamientoVehiculo = comportamientoVehiculo
    def solido(self):
            self.comportamientoVehiculo.carretera()

    def navegar(self):
            self.comportamientoVehiculo.mar()

    def volar(self):
            self.comportamientoVehiculo.cielo()

class Automovil(Mover):
     def __init__(self):
          auto = Tierra()
          super().__init__(auto)

class botemovil(Mover):
    def __init__(self):
         bote = Agua()
         super().__init__(bote)
class Avionmovil(Mover):
     def __init__(self):
          avion = Aire()
          super().__init__(avion)

if __name__ == "__main__":
    vehiculo1 = Automovil()
    print("Auto"), vehiculo1.solido()
    vehiculo2 = botemovil()
    print("Bote: "), vehiculo2.navegar()
    vehiculo3 = Avionmovil()
    print("Avion: "), vehiculo3.volar()
    print()

