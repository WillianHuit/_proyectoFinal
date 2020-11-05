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
        gramatica(tokens)
    menu()

def generarDiagrama():
    print()


def gramatica(tokens):
    pila = ["S","#"]
    foreach= False
    pilaString =""
    faltaCierre = 0
    #27
    pilaString = makePilaString(["Pila"])
    print(pilaString+"|Transicion")
    pilaString = makePilaString(["Λ"])
    print(pilaString+"|(A,Λ,Λ;B,#)")
    entrada = input()
    pilaString = makePilaString(["#"])
    print(pilaString+"|(B,Λ,Λ;C,S)")
    estado = 0
    entrada = input()
    pilaString = makePilaString(pila)
    print(pilaString+"|(B,Λ,Λ;C,S)")
    for i in range(len(tokens)):
        if estado ==0:
            if pila[0] == "S":
                entrada = input()
                if tokens[i][1] == "tk_variable":
                    pila[0:1] = ["ASIGNACION"]
                    pilaString = makePilaString(pila)
                    print(pilaString +"|(Λ,Λ,S;C,ASIGNACION)")
                    estado = 1
                elif tokens[i][1] == "tk_if":
                    pila[0:1] = ["IF"]
                    pilaString = makePilaString(pila)
                    print(pilaString +"|(Λ,Λ,S;C,IF)")
                    estado = 2
                elif tokens[i][1] == "tk_switch":
                    pila[0:1] = ["SWITCH"]
                    pilaString = makePilaString(pila)
                    print(pilaString +"|(Λ,Λ,S;C,SWITCH)")
                    estado = 3
                elif tokens[i][1] == "tk_for":
                    pila[0:1] = ["FOREACH"]
                    foreach = True
                    pilaString = makePilaString(pila)
                    print(pilaString +"|(Λ,Λ,S;C,FOREACH)")
                    estado = 2
                elif tokens[i][1] == "tk_while":
                    pila[0:1] = ["WHILE"]
                    pilaString = makePilaString(pila)
                    print(pilaString +"|(Λ,Λ,S;C,WHILE)")
                    estado = 2
                elif tokens[i][1] == "tk_idVariable":
                    pila[0:1] = ["LLAMADA_FUNCION"]
                    pilaString = makePilaString(pila)
                    print(pilaString +"|(Λ,Λ,S;C,LLAMADA_FUNCION)")
                    estado = 1
                else:
                    entrada = input()
                    pila[0:1] = []
                    pilaString = makePilaString(pila)
                    print(pilaString + "|(C,S, S;C,S,Λ)")
                if tokens[i][1] == "tk_corcheteC" and pila[0] == "}" and faltaCierre > 0:
                    faltaCierre = faltaCierre - 1
                    entrada = input()
                    pila[0:1] = ["S"]
                    pilaString = makePilaString(pila)
                    print(pilaString + "|(C,}, };C,},S)")
                    entrada = input()

        if estado == 1:
            if pila[0] == "ASIGNACION":
                entrada = input()
                pila[0:1] = []
                pila = ["TIPO_VARIABLE", "tk_idVariable", "=", "VALOR",";"] + pila
                pilaString = makePilaString(pila)
                print(pilaString +"|(C,ASIGNACION,ASIGNACION;C,TIPO_VARIABLE tk_idVariable = VALOR;)")
            if tokens[i][1]=="tk_variable" and pila[0]=="TIPO_VARIABLE":
                entrada = input()
                pila[0:1] = ["tk_variable"]
                pilaString = makePilaString(pila)
                print(pilaString +"|(C,TIPO_VARIABLE,TIPO_VARIABLE;C,TIPO_VARIABLE, tk_variable)")
            if pila[0]=="tk_variable":
                entrada = input()
                pila[0:1] = []
                pilaString = makePilaString(pila)
                print(pilaString +"|(C,tk_variable, tk_variable;C,tk_variable,Λ)")
            if tokens[i][1]=="tk_idVariable" and pila[0]=="tk_idVariable":
                entrada = input()
                pila[0:1] = []
                pilaString = makePilaString(pila)
                print(pilaString +"|(C,tk_idVariable, tk_idVariable;C,tk_idVariable , Λ)")
            if tokens[i][1] == "tk_igualdad" and pila[0] == "=":
                entrada = input()
                pila[0:1] = []
                pilaString = makePilaString(pila)
                print(pilaString + "|(C,=, =;C,= , Λ)")
            if pila[0]=="VALOR":
                if tokens[i][1]=="tk_booleano" or tokens[i][1]=="tk_numerico" or tokens[i][1]=="tk_cadena":
                    entrada = input()
                    pila[0:1] = [tokens[i][1]]
                    pilaString = makePilaString(pila)
                    print(pilaString + "|(C,VALOR, VALOR;C,VALOR , "+tokens[i][1]+")")
                    pila[0:1] = []
                    entrada = input()
                    pilaString = makePilaString(pila)
                    print(pilaString + "|(C,"+tokens[i][1]+", "+tokens[i][1]+";C,"+tokens[i][1]+" , Λ)")
            if pila[0] == ";" and tokens[i][1]=="tk_puntoComa":
                pila[0:1] = []
                entrada = input()
                pila = ["S"] + pila
                pilaString = makePilaString(pila)
                estado = 0
                print(pilaString + "|(C,;, ;;C,; , S)")
                entrada = input()

        if estado == 2:
            if pila[0] == "IF":
                entrada = input()
                pila[0:1] = []
                pila = ["tk_if","(","VALOR_TIPO2",")","{","S","}"] + pila
                pilaString = makePilaString(pila)
                print(pilaString + "|(C,IF, IF;C,IF , tk_if(VALOR_TIPO2){S})")
                entrada = input()
                pila[0:1] = []
                pilaString = makePilaString(pila)
                print(pilaString + "|(C,tk_if, tk_if;C,tk_if, Λ")
            if pila[0] == "WHILE":
                entrada = input()
                pila[0:1] = []
                pila = ["tk_while","(","VALOR_TIPO2",")","{","S","}"] + pila
                pilaString = makePilaString(pila)
                print(pilaString + "|(C,WHILE, WHILE;C,WHILE , tk_while(VALOR_TIPO2){S})")
                entrada = input()
                pila[0:1] = []
                pilaString = makePilaString(pila)
                print(pilaString + "|(C,tk_while, tk_while;C,tk_while, Λ")
            if pila[0] == "FOREACH":
                entrada = input()
                pila[0:1] = []
                pila = ["tk_for","(","tk_idVariable","tk_idVariable","tk_idVariable",")","{","S","}"] + pila
                pilaString = makePilaString(pila)
                print(pilaString + "|(C,FOREACH, FOREACH;C,FOREACH , tk_for(tk_idVariable in tk_idVariable){S})")
                entrada = input()
                pila[0:1] = []
                pilaString = makePilaString(pila)
                print(pilaString + "|(C,tk_for, tk_for;C,tk_for, Λ")

            if pila[0] == "(" and tokens[i][1]=="tk_parentesisA":
                entrada = input()
                pila[0:1] = []
                pilaString = makePilaString(pila)
                print(pilaString + "|(C,(, (;C,(, Λ")
            if pila[0]=="VALOR_TIPO2":
                if tokens[i][1]=="tk_booleano" or tokens[i][1]=="tk_idVariable":
                    entrada = input()
                    pila[0:1] = [tokens[i][1]]
                    pilaString = makePilaString(pila)
                    print(pilaString + "|(C,VALOR_TIPO2, VALOR_TIPO2;C,VALOR_TIPO2 , "+tokens[i][1]+")")
                    pila[0:1] = []
                    entrada = input()
                    pilaString = makePilaString(pila)
                    print(pilaString + "|(C,"+tokens[i][1]+", "+tokens[i][1]+";C,"+tokens[i][1]+" , Λ)")
            if pila[0]=="tk_idVariable" and tokens[i][1]=="tk_idVariable":
                entrada = input()
                pila[0:1] = []
                pilaString = makePilaString(pila)
                print(pilaString + "|(C, tk_idVariable, tk_idVariable;C,tk_idVariable, Λ")

            if pila[0]=="in" and tokens[i][0]=="tk_idVariable":
                entrada = input()
                pila[0:1] = []
                pilaString = makePilaString(pila)
                print(pilaString + "|(C, in, in;C,in, Λ")

            if pila[0]==")" and tokens[i][1]=="tk_parentesisC":
                entrada = input()
                pila[0:1] = []
                pilaString = makePilaString(pila)
                print(pilaString + "|(C,), );C,), Λ")

            if pila[0]=="{" and tokens[i][1]=="tk_corcheteA":
                entrada = input()
                pila[0:1] = []
                pilaString = makePilaString(pila)
                print(pilaString + "|(C,{, {;C,}, Λ")
                faltaCierre = faltaCierre + 1
                estado = 0

def makePilaString(pila):
    espacio = ""
    pilaString = ""
    for x in pila:
        pilaString = pilaString + x

    for i in range(50-len(pilaString)):
        espacio = espacio + " "

    pilaString = pilaString + espacio

    return pilaString

if __name__ == '__main__':
    inicio()