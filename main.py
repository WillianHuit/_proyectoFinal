import AFD

script = ""

def inicio():
    print("Bienvenido a Basilisk")
    menu()

def menu():
    print("Selecciona una opción:")
    print("1. Cargar Script")
    print("2. Manejo AFD")
    print("3. Pila Interactiva")
    print("4. Diagrama de Bloques de Código")
    entrada = input()
    opciones(entrada)

def opciones(entrada):
    if entrada == "1":
        cargarScript()
    elif entrada == "2":
        manejoAFD()
    elif entrada == "3":
        pilaInteractiva()
    elif entrada == "4":
        generarDiagrama()
    else:
        error()

def error():
    print("La opción seleccionada no es valida intenta de nuevo")
    menu()

def cargarScript():
    global script
    print("Ingresa la direccion del documento, (ingresa 0 para regresar)")
    entrada = input()
    if entrada == "0":
        menu()
    elif entrada !="":
        try:
            script = ""
            archivo = open(entrada, "r")
            for linea in archivo.readlines():
                script = script + linea
            archivo.close()
            print("-> Se ha almacenado el archivo")
        except:
            print("-> Ocurrio un error seguro que la dirección es: "+entrada)
        menu()
    else:
        print("-> No se realizaron cambios")
        menu()

def manejoAFD():
    global script
    if script == "":
        print("-> El script esta vacio")
    else:
        AFD.manejo(script,True)
    menu()
def pilaInteractiva():
    global script
    tokens = []
    if script == "":
        print("-> El script esta vacio")
    else:
        tokens=AFD.manejo(script, False)
        for i in range(len(tokens)):
            print(tokens[i])
    menu()

def generarDiagrama():
    print()
if __name__ == '__main__':
    inicio()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
