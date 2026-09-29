from abc import ABC, abstractmethod


class estrategiaDescuento(ABC):
    @abstractmethod
    def aplicar(self, pecio_base):
        pass

class sinDescuento(estrategiaDescuento):
    def aplicar(self, precio_base):
        return precio_base

class descuentoVIP(estrategiaDescuento):
    def aplicar(self, precio_base):
        VIP_precio = precio_base-(precio_base*0.8)
        return VIP_precio

class descuentoEstudiante(estrategiaDescuento):
    def aplicar(self, precio_base):
        Estud_descuento = precio_base -(precio_base*0.05)
        return Estud_descuento

class descuentoEmpleado(estrategiaDescuento):
    def aplicar(self, precio_base):
        empleadoPrecio = precio_base -(precio_base*0.25)
        return empleadoPrecio

class compra:
    def __init__(self, estrategiaDescuento):
        self.estrategiaDescuento = estrategiaDescuento

    def calcularTotal(self, precio):
        return self.estrategiaDescuento.aplicar(precio)



def main():
    sin_Descuento = sinDescuento()
    descuento_VIP = descuentoVIP()
    descuento_Estudiante = descuentoEstudiante()
    descuento_Empleado = descuentoEmpleado()

    compra_1 =compra(sin_Descuento)
    print("Total a cobrar: ", compra_1.calcularTotal(100), " Sin descuento.")

    compra_2 =compra(descuento_VIP)
    print("Total a cobrar: ", compra_2.calcularTotal(1000), "Con descuento VIP.")

    compra_3 =compra(descuento_Estudiante)
    print("Total a cobrar: ", compra_3.calcularTotal(10), " Con descuento Estudiante.")

    compra_4 = compra(descuento_Empleado)
    print("total a cobrar: ", compra_4.calcularTotal(100), "Con descuento de empleado.")
main()