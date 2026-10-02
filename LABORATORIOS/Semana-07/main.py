from game_patterns import GameFacade

def main():
    print("===================================")
    print(" VIDEOJUEGO POR TURNOS - LABORATORIO 7 ")
    print("===================================")
    print("Selecciona el mundo para jugar:")
    print("1. Fantasía (Guerrero vs Dragón)")
    print("2. Ciencia Ficción (Soldado vs Alien)")
    
    opcion = input("Ingresa 1 o 2: ")
    while opcion not in ["1", "2"]:
        opcion = input("Opción no válida. Ingresa 1 o 2: ")
    juego = GameFacade()
    juego.crear_mundo_y_personajes(opcion)
    juego.ejecutar_turnos()

if __name__ == "__main__":
    main()