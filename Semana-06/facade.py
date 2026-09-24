class inventario:
    def verificar(self, producto):
        print("verificando stock: ", producto)
        return True

class pago:
    def procesar(self, monto):
        print("Procesando pago: ", monto)
        return True
    
class envio:
    def crearEnvio(self, producto):
        print("preparando envio: ", producto)
        return True

class notificacion:
    def enviarNotificacion(self, producto):
        print("Su compra de ", producto, " Se ha realizado con exito.")


class tiendaFacade:
    def __init__(self):
        self.inventario = inventario()
        self.pago = pago()
        self.envio= envio()
        self.notificacion = notificacion()

    def comprar(self, producto, precio):
        if not self.inventario.verificar(producto):
            print("No hay stock")
            return 

        if not self.pago.procesar(precio):
            print("Fallo el pago")
            return
        self.envio.crearEnvio(producto)
        print("Compra completada")
        return self.notificacion.enviarNotificacion(producto)
def main():
    tienda1 =tiendaFacade()
    tienda1.comprar('laptop', 1500)

main()

