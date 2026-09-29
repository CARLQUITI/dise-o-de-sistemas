from abc import ABC, abstractmethod

class Boton(ABC):
    @abstractmethod
    def renderizar(self):
        pass

class menu(ABC):
    @abstractmethod
    def renderizar(self):
        pass

class checkBox(ABC):
    @abstractmethod
    def renderizar(self):
        pass

class botonWindows(Boton):
    def renderizar(self):
        print("Boton Estilo Windows")
class menuWindows(menu):
    def renderizar(self):
        print("Menu windows")
class checkWindows(checkBox):
    def renderizar(self):
        print("Este estilo es Windows")


class botonMac(Boton):
    def renderizar(self):
        print("Boton Estilo Mac")
class menuMac(menu):
    def renderizar(self):
        print("menu Mac")
class checkMac(checkBox):
    def renderizar(self):
        print("Este estilo es Mac")


class UIFactoryABC(ABC):
    @abstractmethod
    def crearBoton():
        pass
    @abstractmethod
    def crearMenu():
        pass
    @abstractmethod
    def crearCheck():
        pass

class windowsFactory(UIFactoryABC):
    def crearBoton(self):
        return botonWindows()
    def crearMenu(self):
        return menuWindows()
    def crearCheck(self):
        return checkWindows()

class macFactory(UIFactoryABC):
    def crearBoton(self):
        return botonMac()
    def crearMenu(self):
        return menuMac()
    def crearCheck(self):
        return checkMac()
    

def crearUI(factory: UIFactoryABC):
    boton = factory.crearBoton()
    menu = factory.crearMenu()
    check = factory.crearCheck()

    boton.renderizar()
    menu.renderizar()
    check.renderizar()

def main():
    sistema = 'mac' 

    if sistema == 'windows' :
        factory = windowsFactory()
    elif sistema == 'mac' :
        factory = macFactory()

    crearUI(factory)


main()