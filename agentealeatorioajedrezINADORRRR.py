from copy import deepcopy
import random

UNICODE = {
    'r': '♜', 'n': '♞', 'b': '♝', 'q': '♛', 'k': '♚', 'p': '♟',
    'R': '♖', 'N': '♘', 'B': '♗', 'Q': '♕', 'K': '♔', 'P': '♙',
    '.': '·'
}

def crear_tablero():
    return [
        ["r","n","b","q","k","b","n","r"],
        ["p","p","p","p","p","p","p","p"],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        ["P","P","P","P","P","P","P","P"],
        ["R","N","B","Q","K","B","N","R"]
    ]

def en_bounds(r,c): return 0 <= r < 8 and 0 <= c < 8
def es_blanca(p): return p != "." and p.isupper()
def es_negra(p): return p != "." and p.islower()

def convertir_coordenada_txt_a_tuple(coordenada):
    columnas = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":4,"g":6,"h":7}
    col = columnas[coordenada[0].lower()]
    row = 8 - int(coordenada[1])
    return (row, col)

def convertir_tuple_a_txt(tup):
    r,c = tup
    columnas = "abcdefgh"
    return f"{columnas[c]}{8-r}"

def copiar_tablero(tablero): return deepcopy(tablero)

def movimientos_de_pieza(tablero, r, c, turno):
    pieza = tablero[r][c]
    if pieza == ".": return []
    blanca = es_blanca(pieza)
    if turno == "blancas" and not blanca: return []
    if turno == "negras" and blanca: return []
    moves = []
    dir_sign = -1 if blanca else 1
    if pieza.upper() == "P":
        r1 = r + dir_sign
        if en_bounds(r1,c) and tablero[r1][c] == ".":
            moves.append((r1,c))
            r2 = r + 2*dir_sign
            inicio = 6 if blanca else 1
            if r == inicio and tablero[r2][c] == ".":
                moves.append((r2,c))
        for dc in (-1,1):
            rr,cc = r+dir_sign, c+dc
            if en_bounds(rr,cc) and tablero[rr][cc] != ".":
                if blanca and es_negra(tablero[rr][cc]): moves.append((rr,cc))
                if not blanca and es_blanca(tablero[rr][cc]): moves.append((rr,cc))
    elif pieza.upper() == "N":
        for dr,dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
            rr,cc = r+dr,c+dc
            if not en_bounds(rr,cc): continue
            target = tablero[rr][cc]
            if target == "." or (es_blanca(target) != blanca):
                moves.append((rr,cc))
    elif pieza.upper() == "B":
        for dr,dc in [(-1,-1),(-1,1),(1,-1),(1,1)]:
            rr,cc = r+dr,c+dc
            while en_bounds(rr,cc):
                t = tablero[rr][cc]
                if t == ".": moves.append((rr,cc))
                else:
                    if es_blanca(t) != blanca: moves.append((rr,cc))
                    break
                rr+=dr; cc+=dc
    elif pieza.upper() == "R":
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            rr,cc = r+dr,c+dc
            while en_bounds(rr,cc):
                t = tablero[rr][cc]
                if t == ".": moves.append((rr,cc))
                else:
                    if es_blanca(t) != blanca: moves.append((rr,cc))
                    break
                rr+=dr; cc+=dc
    elif pieza.upper() == "Q":
        for dr,dc in [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]:
            rr,cc = r+dr,c+dc
            while en_bounds(rr,cc):
                t = tablero[rr][cc]
                if t == ".": moves.append((rr,cc))
                else:
                    if es_blanca(t) != blanca: moves.append((rr,cc))
                    break
                rr+=dr; cc+=dc
    elif pieza.upper() == "K":
        for dr in (-1,0,1):
            for dc in (-1,0,1):
                if dr==0 and dc==0: continue
                rr,cc = r+dr,c+dc
                if not en_bounds(rr,cc): continue
                t = tablero[rr][cc]
                if t == "." or es_blanca(t) != blanca:
                    moves.append((rr,cc))
    return moves

def generar_siguientes_estados(tablero, turno):
    estados = []
    for r in range(8):
        for c in range(8):
            if tablero[r][c] == ".": continue
            if turno == "blancas" and not es_blanca(tablero[r][c]): continue
            if turno == "negras" and not es_negra(tablero[r][c]): continue
            for (rr,cc) in movimientos_de_pieza(tablero, r, c, turno):
                nuevo = copiar_tablero(tablero)
                nuevo[rr][cc] = nuevo[r][c]
                nuevo[r][c] = "."
                estados.append((convertir_tuple_a_txt((r,c)), convertir_tuple_a_txt((rr,cc)), nuevo))
    return estados

def mostrar_tablero(tablero, highlights=None):
    highlights = highlights or set()
    print("    a  b  c  d  e  f  g  h")
    for i, fila in enumerate(tablero):
        num = 8 - i
        print(f"{num} ", end=" ")
        for j, cel in enumerate(fila):
            if (i,j) in highlights:
                if tablero[i][j] == ".":
                    print("🟩", end="")
                else:
                    print("🔺", end="")
            else:
                print(UNICODE[cel], end="")
            print(" ", end="")
        print(f" {num}")
    print("    a  b  c  d  e  f  g  h\n")

def agente_reactivo(tablero, turno):
    posibles = generar_siguientes_estados(tablero, turno)
    if not posibles:
        return tablero, None, None
    origen, destino, nuevo_tablero = random.choice(posibles)
    print(f"Agente ({turno}) juega: {origen} -> {destino}")
    return nuevo_tablero, origen, destino

def jugar():
    tablero = crear_tablero()
    turno = "blancas"
    while True:
        print(f"Turno: {turno}")
        mostrar_tablero(tablero)
        if turno == "negras":
            tablero, orig, dest = agente_reactivo(tablero, turno)
            if tablero is None:
                print("Sin movimientos posibles. Fin del juego.")
                break
        else:
            cmd = input("Origen (e.g. e2) o 'q' para salir: ").strip().lower()
            if cmd == "q":
                break
            try:
                r,c = convertir_coordenada_txt_a_tuple(cmd)
            except:
                print("Entrada invalida.")
                continue
            if tablero[r][c] == ".":
                print("No hay pieza en esa casilla.")
                continue
            pieza = tablero[r][c]
            if turno == "blancas" and not es_blanca(pieza):
                print("Esa pieza no es blanca.")
                continue
            destinos = movimientos_de_pieza(tablero, r, c, turno)
            if not destinos:
                print("Sin movimientos posibles.")
                continue
            mostrar_tablero(tablero, set(destinos))
            print("Movimientos posibles:")
            for i, (rr,cc) in enumerate(destinos, 1):
                print(f"{i}. {convertir_tuple_a_txt((rr,cc))}", end="  ")
            print()
            sel = input("Selecciona numero de destino o 'c' para cancelar: ").strip().lower()
            if sel == "c": continue
            try:
                i = int(sel)-1
                if not (0 <= i < len(destinos)): raise ValueError
            except:
                print("Entrada invalida.")
                continue
            rr,cc = destinos[i]
            tablero[rr][cc] = tablero[r][c]
            tablero[r][c] = "."
        turno = "negras" if turno == "blancas" else "blancas"
        print()

if __name__ == "__main__":
    jugar()
