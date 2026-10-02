import random
from abc import ABC, abstractmethod

class GameConfig:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(GameConfig, cls).__new__(cls)
            cls._instancia.dificultad = "Normal"
            cls._instancia.numero_maximo_turnos = 10
        return cls._instancia


class EstrategiaAtaque(ABC):
    @abstractmethod
    def ejecutar(self, atacante, defensor):
        pass

class AtaqueNormal(EstrategiaAtaque):
    def ejecutar(self, atacante, defensor):
        dano = atacante.ataque
        defensor.vida -= dano
        print(f"⚔️ {atacante.nombre} usa [Ataque Normal] y causa {dano} de daño!")

class AtaqueFuerte(EstrategiaAtaque):
    def ejecutar(self, atacante, defensor):
        if random.random() > 0.3:
            dano = atacante.ataque * 2
            defensor.vida -= dano
            print(f"🔥 {atacante.nombre} usa [Ataque Fuerte] y causa {dano} de daño!")
        else:
            print(f"💨 {atacante.nombre} intentó usar [Ataque Fuerte] pero falló!")

class Personaje:
    def __init__(self, nombre, vida, ataque):
        self.nombre = nombre 
        self.vida = vida 
        self.ataque = ataque 
        self.estrategia = AtaqueNormal() 

    def set_estrategia(self, estrategia):
        self.estrategia = estrategia

    def atacar(self, enemigo):
        self.estrategia.ejecutar(self, enemigo)

class PersonajeFactory:
    @staticmethod
    def crear(tipo):
        if tipo == "guerrero": return Personaje("Guerrero", 100, 15)
        if tipo == "dragon": return Personaje("Dragón", 150, 20)
        if tipo == "soldado": return Personaje("Soldado", 90, 18)
        if tipo == "alien": return Personaje("Alien", 120, 22)
        raise ValueError("Tipo de personaje desconocido")

class AbstractFactory(ABC):
    @abstractmethod
    def crear_jugador(self): pass
    @abstractmethod
    def crear_enemigo(self): pass

class FantasyFactory(AbstractFactory):
    def crear_jugador(self): return PersonajeFactory.crear("guerrero") 
    def crear_enemigo(self): return PersonajeFactory.crear("dragon") 

class SciFiFactory(AbstractFactory):
    def crear_jugador(self): return PersonajeFactory.crear("soldado") 
    def crear_enemigo(self): return PersonajeFactory.crear("alien") 


class GameFacade:
    def __init__(self):
        self.config = GameConfig()
        self.jugador = None
        self.enemigo = None
        self.turno_actual = 0

    def crear_mundo_y_personajes(self, opcion_mundo):
        if opcion_mundo == "1":
            factory = FantasyFactory()
            nombre_mundo = "Fantasía"
        else:
            factory = SciFiFactory()
            nombre_mundo = "Ciencia Ficción"
            
        self.jugador = factory.crear_jugador()
        self.enemigo = factory.crear_enemigo()
        print(f"\n🌍 Mundo de {nombre_mundo} creado.")
        print(f"👤 Jugador: {self.jugador.nombre} vs 👾 Enemigo: {self.enemigo.nombre}")

    def aplicar_estrategia_jugador(self):
        print("\nElige tu estrategia de ataque:")
        print("1. Ataque Normal")
        print("2. Ataque Fuerte")
        opcion = input("Tu elección (1/2): ")
        
        if opcion == "2":
            self.jugador.set_estrategia(AtaqueFuerte())
        else:
            self.jugador.set_estrategia(AtaqueNormal())

    def ejecutar_turnos(self):
        while self.jugador.vida > 0 and self.enemigo.vida > 0 and self.turno_actual < self.config.numero_maximo_turnos:
            self.turno_actual += 1
            print(f"\n--- TURNO {self.turno_actual} ---")
            print(f"[{self.jugador.nombre}: {self.jugador.vida} HP] | [{self.enemigo.nombre}: {self.enemigo.vida} HP]")
            
            self.aplicar_estrategia_jugador()
            self.jugador.atacar(self.enemigo)
            if self.enemigo.vida > 0:
                print("\nTurno del enemigo...")
                self.enemigo.set_estrategia(AtaqueNormal())
                self.enemigo.atacar(self.jugador)
                
        self.determinar_ganador()

    def determinar_ganador(self):
        print("\n" + "="*20)
        print(" FIN DE LA PARTIDA ")
        print("="*20)
        if self.jugador.vida <= 0 and self.enemigo.vida <= 0:
            print("¡Ambos han caído! Es un empate.")
        elif self.jugador.vida <= 0:
            print(f"💀 Has sido derrotado por {self.enemigo.nombre}.")
        elif self.enemigo.vida <= 0:
            print(f"🏆 ¡Victoria! Has derrotado a {self.enemigo.nombre}.")
        else:
            print("⏳ Se alcanzó el límite de turnos. ¡Es un empate!")