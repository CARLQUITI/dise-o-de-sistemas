#vehiculo ->mueva -> mover()

#auto -> mueve por carretera
#bote -> mueve por mar
#Avion -> mueve por cielo

class ComportamientoTierra:
    def solido(self):
        raise NotImplementedError("Este metodo no esta implementado")
class Carretera(ComportamientoTierra):
    def solido(self):
        print("Conduciendo por carretera")
   
class ComportamientoAgua:
    def navegar(self):
        raise NotImplementedError("Este metodo no esta implementado")
class mar(ComportamientoAgua):
    def navegar(self):
        print("Navegando por agua")

class ComportamientoAire:
    def volar(self):
        raise NotImplementedError("Este metodo no esta implementado")
class Cielo(ComportamientoAire):
    def volar(self):
        print("Volando por el cielo")

class Mover:
    def __init__(self, comportamientoTierra, comportamientoAgua, comportamientoAire):
        self.comportamientoTierra = comportamientoTierra
        self.comportamientoAgua = comportamientoAgua
        self.comportamientoAire = comportamientoAire

    def solido(self):
            self.comportamientoTierra.solido()

    def navegar(self):
            self.comportamientoAgua.navegar()

    def volar(self):
            self.comportamientoAire.volar()

class Automovil(Mover):
     def __init__(self):
          auto = Carretera()
          super().__init__(auto, None, None)

class botemovil(Mover):
    def __init__(self):
         bote = mar()
         super().__init__(None, bote, None)
class Avionmovil(Mover):
     def __init__(self):
          avion = Cielo()
          super().__init__(None, None, avion)

if __name__ == "__main__":
    vehiculo1 = Automovil()
    print("Auto: "), vehiculo1.solido()
    vehiculo2 = botemovil()
    print("bote: "),vehiculo2.navegar()
    vehiculo3 = Avionmovil()
    print("avion: "), vehiculo3.volar()
    print()

