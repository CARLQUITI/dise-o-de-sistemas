class comportamientoVuelo:
    def volar(self):
        raise NotImplementedError("Este metodo no esta implementado")

class VuelaConAlas(comportamientoVuelo):
    def volar(self):
        print("volando con alas")

class noVuela(comportamientoVuelo):
    def volar(self):
        print("no vuela")

class comportamientoGraznar:
    def graznar(self):
        raise NotImplementedError("Este metodo no esta implementado")

class graznidonormal(comportamientoGraznar):
    def graznar(self):
        print("CUACK CUACK")

class graznidoDeGoma(comportamientoGraznar):
    def graznar(self):
        print("Chirrido de goma")

class Pato:
    def __init__(self, comportamientoVuelo, comportamientoGraznar):
        self.comportamientoVuelo = comportamientoVuelo
        self.comportamientoGraznar = comportamientoGraznar
    def nadar(self):
        print("nadando")

    def graznar(self):
        self.comportamientoGraznar.graznar()

    def volar(self):
        self.comportamientoVuelo.volar()


class PatoSalvaje(Pato):
    def __init__(self):
        VuelaAlas = VuelaConAlas()
        graznidoN = graznidonormal()
        super().__init__(VuelaAlas, graznidoN)


class PatoDeGoma(Pato):
    def __init__(self):
        novuela= noVuela()
        graznidoG = graznidoDeGoma()
        super().__init__(novuela, graznidoG)

#    def graznar(self):
#        print("Chirrido de goma")

#    def volar(self):      | mala practica
#        print("No vuela")


if __name__ == "__main__":
    salvaje = PatoSalvaje()
    salvaje.nadar()
    salvaje.graznar()
    salvaje.volar()

    print()

    goma = PatoDeGoma()
    goma.nadar()
    goma.graznar()
    goma.volar()