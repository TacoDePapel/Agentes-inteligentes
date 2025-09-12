import random
import os
import time

def crear_ambiente(n):
    ambiente = []
    for i in range(n):
        if random.random() < 0.5:
            ambiente.append("Sucio")
        else:
            ambiente.append("Limpio")
    return ambiente

def mostrar(ambiente, posicion, paso, estrategia, perf):
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Estrategia: {estrategia.upper()} | Paso {paso}")
    print(f"Desempeño parcial: {perf:.2f}")
    fila = ""
    for i in range(len(ambiente)):
        if i == posicion:
            fila += "🤖"
        elif ambiente[i] == "Sucio":
            fila += "🟫"
        else:
            fila += "⬜"
    print(fila)
    print("-" * len(ambiente) * 2)

def medir_desempeno(ambiente):
    limpias = ambiente.count("Limpio")
    return limpias / len(ambiente)

def agente(estrategia, posicion, estado, n, direccion):
    #derecha
    if estrategia == "derecha":
        if estado == "Sucio":
            return "ASPIRAR", direccion
        if posicion == 0:
            direccion = 1
        elif posicion == n - 1:
            direccion = -1
        accion = "DERECHA" if direccion == 1 else "IZQUIERDA"
        return accion, direccion

    #aleatoria
    if estrategia == "aleatorio":
        if estado == "Sucio":
            return "ASPIRAR", direccion
        return random.choice([("IZQUIERDA", direccion), ("DERECHA", direccion)])

    #aspirar primero
    if estrategia == "aspirar_primero":
        if estado == "Sucio":
            return "ASPIRAR", direccion
        return random.choice([("IZQUIERDA", direccion), ("DERECHA", direccion)])

    #racional
    if estrategia == "racional":
        if estado == "Sucio":
            return "ASPIRAR", direccion
        if posicion == 0:
            direccion = 1
        elif posicion == n - 1:
            direccion = -1
        accion = "DERECHA" if direccion == 1 else "IZQUIERDA"
        return accion, direccion

    return "ASPIRAR", direccion

def simular(estrategia, N=5, T=20, animar=False):
    ambiente = crear_ambiente(N)
    posicion = random.randint(0, N - 1)
    direccion = 1
    desempeno_total = 0
    pasos = 0

    for t in range(1, T + 1):
        estado = ambiente[posicion]
        accion, direccion = agente(estrategia, posicion, estado, N, direccion)

        if accion == "ASPIRAR":
            ambiente[posicion] = "Limpio"
        elif accion == "IZQUIERDA" and posicion > 0:
            posicion -= 1
        elif accion == "DERECHA" and posicion < N - 1:
            posicion += 1

        perf = medir_desempeno(ambiente)
        desempeno_total += perf
        pasos += 1

        if animar:
            mostrar(ambiente, posicion, pasos, estrategia, perf)
            time.sleep(0.2)

        if ambiente.count("Sucio") == 0:
            break

    return desempeno_total / pasos

estrategias = ["derecha", "aleatorio", "aspirar_primero", "racional"]
resultados = {}

for e in estrategias:
    val = simular(e, N=5, T=20, animar=False)
    resultados[e] = val

print("\nResultados de desempeño:")
for e, val in resultados.items():
    print(f" - {e}: {val:.2f}")

mejor = max(resultados, key=resultados.get)
print(f"\nLa mejor estrategia fue '{mejor.upper()}'\n")

input("Presiona ENTER para ver la animación de la mejor estrategia...")
simular(mejor, N=5, T=20, animar=True)
