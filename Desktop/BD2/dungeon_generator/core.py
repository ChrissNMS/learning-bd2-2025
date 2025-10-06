from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Optional, List
import random
import json
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

class Habitacion:
    """Representa una habitación dentro del dungeon."""
    def __init__(self, id: int, x: int, y: int, inicial: bool = False):
        self.id = id
        self.x = x
        self.y = y
        self.inicial = inicial
        self.contenido: Optional[ContenidoHabitacion] = None
        self.conexiones: Dict[str, Habitacion] = {}
        self.visitada = False

    def __repr__(self) -> str:
        return f"Habitacion(id={self.id}, pos=({self.x},{self.y}), inicial={self.inicial})"

class Mapa:
    """Representa el mapa completo del dungeon."""
    def __init__(self, ancho: int, alto: int, n_habitaciones: int):
        self.ancho = ancho
        self.alto = alto
        self.habitaciones: Dict[tuple[int, int], Habitacion] = {}
        self.habitacion_inicial: Optional[Habitacion] = None
        self.generar_estructura(n_habitaciones)
        self.colocar_contenido()

    def generar_estructura(self, n_habitaciones: int):
        """Crea la estructura básica del dungeon."""
        if n_habitaciones > self.ancho * self.alto:
            raise ValueError("Demasiadas habitaciones para el tamaño del mapa.")

        coords_disponibles = [(x, y) for x in range(self.ancho) for y in range(self.alto)]
        random.shuffle(coords_disponibles)

        for i in range(n_habitaciones):
            x, y = coords_disponibles.pop()
            habitacion = Habitacion(i, x, y)
            self.habitaciones[(x, y)] = habitacion

        bordes = [(x, y) for (x, y) in self.habitaciones if x in [0, self.ancho - 1] or y in [0, self.alto - 1]]
        inicio_coord = random.choice(bordes)
        self.habitacion_inicial = self.habitaciones[inicio_coord]
        self.habitacion_inicial.inicial = True

        for (x, y), hab in self.habitaciones.items():
            direcciones = {
                "norte": (x, y - 1),
                "sur": (x, y + 1),
                "este": (x + 1, y),
                "oeste": (x - 1, y)
            }
            for dir, (nx, ny) in direcciones.items():
                if (nx, ny) in self.habitaciones:
                    hab.conexiones[dir] = self.habitaciones[(nx, ny)]

    def colocar_contenido(self):
        """Distribuye monstruos, tesoros, eventos y jefes según las reglas."""
        for coords, habitacion in self.habitaciones.items():
            if habitacion.inicial:
                continue
            x, y = coords
            if (x in [0, self.ancho - 1]) and (y in [0, self.alto - 1]):
                habitacion.contenido = Jefe(
                    f"Jefe_{habitacion.id}",
                    vida=6,
                    ataque=3,
                    recompensa_especial=Objeto("Cetro Dorado", 100, "Tesoro legendario")
                )
            else:
                rand = random.random()
                if rand < 0.25:
                    habitacion.contenido = Monstruo(f"Monstruo_{habitacion.id}", vida=3, ataque=1)
                elif rand < 0.45:
                    habitacion.contenido = Tesoro(Objeto(f"Tesorillo_{habitacion.id}", 20, "Objeto brillante"))
                elif rand < 0.55:
                    habitacion.contenido = Evento(random.choice(["Trampa", "Fuente de Vida", "Portal", "Bendición"]))
                else:
                    habitacion.contenido = None

    def obtener_estadisticas_mapa(self) -> dict:
        """Retorna estadísticas del mapa (Requerimiento 7)."""
        total = len(self.habitaciones)
        tipos = {"Monstruo": 0, "Tesoro": 0, "Jefe": 0, "Evento": 0, "Vacia": 0}
        conexiones_totales = 0
        for hab in self.habitaciones.values():
            conexiones_totales += len(hab.conexiones)
            if hab.contenido is None:
                tipos["Vacia"] += 1
            else:
                tipos[hab.contenido.tipo] = tipos.get(hab.contenido.tipo, 0) + 1
        promedio_conexiones = conexiones_totales / total
        return {"total_habitaciones": total, **tipos, "promedio_conexiones": promedio_conexiones}

@dataclass
class Objeto:
    nombre: str
    valor: int
    descripcion: str

class Explorador:
    """Representa al jugador explorador dentro del dungeon."""
    def __init__(self, mapa: Mapa):
        self.vida = 5
        self.inventario: List[Objeto] = []
        self.mapa = mapa
        self.posicion_actual = (mapa.habitacion_inicial.x, mapa.habitacion_inicial.y)

    @property
    def esta_vivo(self) -> bool:
        return self.vida > 0

    def recibir_dano(self, cantidad: int):
        self.vida = max(0, self.vida - cantidad)

    def mover(self, direccion: str) -> bool:
        habitacion_actual = self.mapa.habitaciones[self.posicion_actual]
        if direccion in habitacion_actual.conexiones:
            nueva = habitacion_actual.conexiones[direccion]
            self.posicion_actual = (nueva.x, nueva.y)
            return True
        return False

    def explorar_habitacion(self) -> str:
        hab = self.mapa.habitaciones[self.posicion_actual]
        hab.visitada = True
        if hab.contenido:
            return hab.contenido.interactuar(self)
        return "No hay nada interesante aquí."

    def obtener_habitaciones_adyacentes(self) -> list[str]:
        hab = self.mapa.habitaciones[self.posicion_actual]
        return list(hab.conexiones.keys())

class ContenidoHabitacion(ABC):
    """Contenido dentro de una habitación (abstracta)."""
    @property
    @abstractmethod
    def descripcion(self) -> str: ...
    @property
    @abstractmethod
    def tipo(self) -> str: ...
    @abstractmethod
    def interactuar(self, explorador: Explorador) -> str: ...

class Tesoro(ContenidoHabitacion):
    def __init__(self, recompensa: Objeto):
        self.recompensa = recompensa

    @property
    def descripcion(self) -> str:
        return f"Tesoro con {self.recompensa.nombre}"

    @property
    def tipo(self) -> str:
        return "Tesoro"

    def interactuar(self, explorador: Explorador) -> str:
        explorador.inventario.append(self.recompensa)
        return f"Has recogido un {self.recompensa.nombre} con valor {self.recompensa.valor}."


class Monstruo(ContenidoHabitacion):
    def __init__(self, nombre: str, vida: int, ataque: int):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque

    @property
    def descripcion(self) -> str:
        return f"Monstruo {self.nombre} (vida={self.vida}, ataque={self.ataque})"

    @property
    def tipo(self) -> str:
        return "Monstruo"

    def interactuar(self, explorador: Explorador) -> str:
        combate = []
        while self.vida > 0 and explorador.vida > 0:
            if random.random() < 0.5:
                self.vida -= 1
                combate.append(f"Golpeas al {self.nombre}. Vida restante: {self.vida}")
            else:
                explorador.recibir_dano(self.ataque)
                combate.append(f"El {self.nombre} te ataca. Tu vida: {explorador.vida}")
        if self.vida <= 0:
            combate.append(f"Has derrotado al {self.nombre}!")
        else:
            combate.append(f"Has sido derrotado por el {self.nombre}...")
        return "\n".join(combate)


class Jefe(Monstruo):
    def __init__(self, nombre: str, vida: int, ataque: int, recompensa_especial: Objeto):
        super().__init__(nombre, vida, ataque)
        self.recompensa_especial = recompensa_especial

    @property
    def tipo(self) -> str:
        return "Jefe"

    def interactuar(self, explorador: Explorador) -> str:
        combate = []
        while self.vida > 0 and explorador.vida > 0:
            if random.random() < 0.3:
                self.vida -= 1
                combate.append(f"Golpeas al jefe {self.nombre}. Vida restante: {self.vida}")
            else:
                explorador.recibir_dano(self.ataque)
                combate.append(f"El jefe {self.nombre} te ataca. Tu vida: {explorador.vida}")
        if self.vida <= 0:
            explorador.inventario.append(self.recompensa_especial)
            if random.random() < 0.3:
                explorador.inventario.append(self.recompensa_especial)
                combate.append("¡Has obtenido una doble recompensa especial!")
            combate.append(f"Has derrotado al jefe {self.nombre}!")
        else:
            combate.append(f"Has sido derrotado por el jefe {self.nombre}...")
        return "\n".join(combate)

class Visualizador:
    def __init__(self, mapa: Mapa, explorador: Explorador):
        self.console = Console()
        self.mapa = mapa
        self.explorador = explorador

    def mostrar_mapa_completo(self):
        text = Text()
        for y in range(self.mapa.alto):
            for x in range(self.mapa.ancho):
                if (x, y) not in self.mapa.habitaciones:
                    text.append("   ", style="on grey15")
                    continue
                hab = self.mapa.habitaciones[(x, y)]
                if (x, y) == self.explorador.posicion_actual:
                    symbol, color = "@", "bright_green"
                elif hab.inicial:
                    symbol, color = "S", "bright_blue"
                elif hab.contenido is None:
                    symbol, color = ".", "dim white"
                elif hab.contenido.tipo == "Monstruo":
                    symbol, color = "E", "red"
                elif hab.contenido.tipo == "Tesoro":
                    symbol, color = "$", "yellow"
                elif hab.contenido.tipo == "Jefe":
                    symbol, color = "X", "magenta"
                elif hab.contenido.tipo == "Evento":
                    symbol, color = "?", "cyan"
                else:
                    symbol, color = "?", "white"
                text.append(f" {symbol} ", style=color)
            text.append("\n")
        panel = Panel(Align.center(text), title="🗺  Mapa del Dungeon", border_style="cyan")
        self.console.print(panel)

    def mostrar_estado_explorador(self):
        inv = ", ".join(obj.nombre for obj in self.explorador.inventario) or "Vacío"
        panel = Panel(
            f"Vida: {self.explorador.vida}\nInventario: {inv}",
            title="Estado del Explorador", border_style="green"
        )
        self.console.print(panel)

def guardar_partida(mapa: Mapa, explorador: Explorador, archivo: str):
    """Guarda partida en formato JSON o YAML."""
    data = {
        "nombre": "Dungeon v1.0",
        "mapa": {
            "ancho": mapa.ancho,
            "alto": mapa.alto,
            "habitaciones": [
                {
                    "id": hab.id,
                    "x": hab.x,
                    "y": hab.y,
                    "inicial": hab.inicial,
                    "visitada": hab.visitada,
                    "contenido": hab.contenido.tipo if hab.contenido else None,
                }
                for hab in mapa.habitaciones.values()
            ],
        },
        "explorador": {
            "vida": explorador.vida,
            "posicion_actual": explorador.posicion_actual,
            "inventario": [obj.__dict__ for obj in explorador.inventario],
        },
    }
    if archivo.endswith(".json"):
        json.dump(data, open(archivo, "w"), indent=2)
    elif archivo.endswith(".yaml") or archivo.endswith(".yml"):
        yaml.dump(data, open(archivo, "w"))
    else:
        raise ValueError("Formato no soportado (usa .json o .yaml)")

class Evento(ContenidoHabitacion):
    def __init__(self, tipo_evento: str):
        self.tipo_evento = tipo_evento

    @property
    def descripcion(self) -> str:
        return f"Evento especial: {self.tipo_evento}"

    @property
    def tipo(self) -> str:
        return "Evento"

    def interactuar(self, explorador: Explorador) -> str:
        if self.tipo_evento == "Trampa":
            explorador.recibir_dano(1)
            return "💀 ¡Has caído en una trampa! Pierdes 1 punto de vida."
        elif self.tipo_evento == "Fuente de Vida":
            explorador.vida = min(10, explorador.vida + 2)
            return "💧 Encuentras una fuente de vida. Recuperas 2 puntos de vida."
        elif self.tipo_evento == "Portal":
            destino = random.choice(list(explorador.mapa.habitaciones.keys()))
            explorador.posicion_actual = destino
            return f"🌪 ¡Un portal te transporta mágicamente a {destino}!"
        elif self.tipo_evento == "Bendición":
            explorador.inventario.append(Objeto("Amuleto Sagrado", 50, "Aumenta la suerte"))
            return "✨ Recibes una bendición y obtienes un Amuleto Sagrado."
        else:
            return "No pasa nada..."

def distancia_manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Calcula la distancia Manhattan entre dos habitaciones."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def ajustar_dificultad(mapa: Mapa):
    """Aumenta la dificultad de enemigos según la distancia a la habitación inicial."""
    inicio = (mapa.habitacion_inicial.x, mapa.habitacion_inicial.y)
    for (x, y), hab in mapa.habitaciones.items():
        dist = distancia_manhattan(inicio, (x, y))
        if isinstance(hab.contenido, Monstruo):
            hab.contenido.vida += dist // 2
            hab.contenido.ataque += dist // 3
        elif isinstance(hab.contenido, Jefe):
            hab.contenido.vida += dist
            hab.contenido.ataque += dist // 2
