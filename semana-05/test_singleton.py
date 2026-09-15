from singleton import GestorDeConfiguracion, reserva_permitida

def test_rechaza_reserva():
    config = GestorDeConfiguracion.obtener_objeto
    config.modo_mantenimiento = False

    assert reserva_permitida(config) is True

def test_reserva_aceptada():
    config = GestorDeConfiguracion.obtener_objeto

    assert reserva_permitida(config) is True

#Este falla porque el objeto está siendo tomado como una variable global dentro de test_singleton.py entonces al modificarse, una y otra vez cambia según
#el objeto vaya pasando por las funciones y según se vaya modificando porque al final no esta creando un nuevo objeto o instancia sino reutilizando 
# la misma de sigleton.py