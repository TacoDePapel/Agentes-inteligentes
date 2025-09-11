import random

class Entorno:
    def __init__(self):
        self.habitaciones = {
            "A": random.choice(["limpio", "sucio"]),
            "B": random.choice(["limpio", "sucio"])
        }
        self.ubicacion_agente = "A"

    def percibir(self):
        return self.ubicacion_agente, self.habitaciones[self.ubicacion_agente]

    def ejecutar_accion(self, accion):
        if accion == "aspirar":
            self.habitaciones[self.ubicacion_agente] = "limpio"
        elif accion == "izquierda":
            self.ubicacion_agente = "A"
        elif accion == "derecha":
            self.ubicacion_agente = "B"

class AgenteAspiradora:
    def programa(self, percepcion):
        ubicacion, estado = percepcion
        if estado == "sucio":
            return "aspira"
        elif ubicacion == "A":
            return "derecha"
        else:
            return "izquierda"

entorno = Entorno()
agente = AgenteAspiradora()

print("Estado inicial:", entorno.habitaciones, "Agente en:", entorno.ubicacion_agente)

for i in range(4):
    percepcion = entorno.percibir()
    accion = agente.programa(percepcion)
    entorno.ejecutar_accion(accion)
    print(f"Paso {i+1}: Percepción={percepcion}, Acción={accion}")
    print("Habitaciones:", entorno.habitaciones, "Agente en:", entorno.ubicacion_agente)
