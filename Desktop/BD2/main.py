from dungeon_generator.core import Mapa, Explorador, Visualizador, guardar_partida

if __name__ == "__main__":
    mapa = Mapa(ancho=5, alto=5, n_habitaciones=12)
    explorador = Explorador(mapa)
    visual = Visualizador(mapa, explorador)

    visual.mostrar_mapa_completo()
    visual.mostrar_estado_explorador()
    print("\nHabitaciones adyacentes:", explorador.obtener_habitaciones_adyacentes())
    print(explorador.explorar_habitacion())

    guardar_partida(mapa, explorador, "partida.json")
    print("\nPartida guardada en partida.json")
