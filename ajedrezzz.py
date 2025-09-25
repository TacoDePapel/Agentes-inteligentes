def crear_tablero():
    tablero = [
        ["r","n","b","q","k","b","n","r"],
        ["p","p","p","p","p","p","p","p"],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        [".",".",".",".",".",".",".","."],
        ["P","P","P","P","P","P","P","P"],
        ["R","N","B","Q","K","B","N","R"]
    ]
    return tablero

def mostrar_tablero(tablero):
    print("  a b c d e f g h")
    for i, fila in enumerate(tablero):
        print(str(8 - i) + " " + " ".join(fila) + " " + str(8 - i))
    print("  a b c d e f g h\n")

def convertir_coordenada(coordenada):
    columnas = {"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7}
    fila = 8 - int(coordenada[1])
    col = columnas[coordenada[0]]
    return (fila, col)

def mover_pieza(tablero, origen_txt, destino_txt, turno):
    origen = convertir_coordenada(origen_txt)
    destino = convertir_coordenada(destino_txt)

    fila_o, col_o = origen
    fila_d, col_d = destino
    pieza = tablero[fila_o][col_o]

    if pieza == ".":
        print("❌ No hay pieza en la casilla de origen.")
        return tablero, turno

    if turno == "blancas" and pieza.islower():
        print("❌ No puedes mover piezas negras en el turno de blancas.")
        return tablero, turno
    if turno == "negras" and pieza.isupper():
        print("❌ No puedes mover piezas blancas en el turno de negras.")
        return tablero, turno

    tablero[fila_o][col_o] = "."
    tablero[fila_d][col_d] = pieza

    turno = "negras" if turno == "blancas" else "blancas"
    return tablero, turno

tablero = crear_tablero()
turno = "blancas"

mostrar_tablero(tablero)

tablero, turno = mover_pieza(tablero, "e2", "e4", turno)
mostrar_tablero(tablero)

tablero, turno = mover_pieza(tablero, "e7", "e5", turno)
mostrar_tablero(tablero)

tablero, turno = mover_pieza(tablero, "e7", "e6", turno)
