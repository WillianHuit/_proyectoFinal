#"if" - tk_if - palabra reservada if - fila:5 - columna:10
#tk_{ tk_} tk_( tk_) tk_true tk_false
import webbrowser
parametros = False
txtPrueba = "funcion1(4,true,variable1);"
#switch ( identificador ) {case 1 :/* Instrucciones */break ;default :/* Instrucciones */break ;}

reservado = [["let","tk_variable","palabra reservada variable"],["var","tk_variable","palabra reservada variable"],
             ["const","tk_variable","palabra reservada variable"],["if","tk_if","palabra reservada if"],
             ["while","tk_while","Palabra reservada while"],["foreach","tk_for","Palabra reservada for"],
             ["switch","tk_switch","Palabra reservada switch"],
             ["(","tk_parentesis","parentesis de apertura"],[")","tk_parentesis","parentesis de cierre"],["{","tk_corchete","corchete de apertura"],
             ["}","tk_corchete","corchete de cierre"],[";","tk_comillas","Simbolo delimitador"],
             ["=>","tk_flecha","Simbolo flecha"],["=","tk_igualdad","Simbolo de igualdad"],[":","tk_puntos","Simbolo de continuidad"],[",","tk_coma","Simbolo separador"],
             ["break","tk_break","Finaliza un caso"],["case","tk_case","Opción de un switch"],["default","tk_default","Opción Switch"]]
tokens = []
error = []

def manejo(entrada,imprimir):
    global tokens
    global parametros
    fila = 1
    columna = 0
    estado = 0
    temp = ""
    digito = ""
    contador = 0
    insertadoInto = -1
    temp2=""
    passEquals = False
    for i in range(len(entrada)):
        columna = columna + 1
        if entrada[i] =="\n":
            fila = fila + 1
            columna = 1
        if estado == 0:
            if entrada[i]==" ":
                if temp != "" or digito != "":
                    if digito != "":
                        tokens = tokens + [[digito, "tk_numerico", "Valor numerico asignado"] + [fila, columna]]
                        digito=""
                    if temp == "false" or temp == "true":
                        tokens = tokens + [[temp, "tk_booleano", "Valor reservado booleano"] + [fila, columna]]
                        temp=""
                    elif temp!="":
                        valor = insertarValor(temp, fila, columna)
                        if valor[0] and passEquals:
                            insertadoInto = valor[1]
                            passEquals = False

                temp = ""
                digito = ""

            if simboloPerteneciente(entrada[i], fila, columna)[0]:
                    if entrada[i]=="=" and entrada[i+1]!=">":
                        if temp != "" or digito != "":
                            if digito != "":
                                tokens = tokens + [[digito, "tk_numerico", "Valor numerico asignado"] + [fila, columna]]
                                digito = ""
                            if temp == "false" or temp == "true":
                                tokens = tokens + [[temp, "tk_booleano", "Valor reservado booleano"] + [fila, columna]]
                                temp = ""
                            elif temp != "":
                                valor = insertarValor(temp, fila, columna)
                                print(valor)
                                if valor[0] and passEquals:
                                    insertadoInto = valor[1]
                                    passEquals = False

                        temp = ""
                        digito = ""
                        tokens = tokens + simboloPerteneciente(entrada[i], fila, columna)[1]
                    elif entrada[i]!="=":
                        if simboloPerteneciente(entrada[i], fila, columna)[0]:
                            if temp != "" or digito != "":
                                if digito != "":
                                    tokens = tokens + [[digito, "tk_numerico", "Valor numerico asignado"] + [fila, columna]]
                                if temp == "false" or temp == "true":
                                    tokens = tokens + [
                                        [temp, "tk_booleano", "Valor reservado booleano"] + [fila, columna]]
                                elif temp!="":
                                    valor = insertarValor(temp, fila, columna)
                                    if valor[0] and passEquals:
                                        insertadoInto = valor[1]
                                        passEquals= False

                                temp = ""
                                digito = ""
                            tokens = tokens + simboloPerteneciente(entrada[i], fila, columna)[1]


            elif entrada[i]==">" and entrada[i-1]=="=":
                tokens = tokens + [["=>","tk_flecha","Simbolo flecha"]+[fila,columna]]
                if insertadoInto != -1:
                    tokens[insertadoInto][1] = "tk_funcion"
                    tokens[insertadoInto][2] = "Id de una función"
                    insertadoInto = -1
            elif entrada[i] == "/":
                estado = 1
            elif entrada[i]=="\"":
                estado = 2
            elif entrada[i] == "_" or entrada[i].isalpha() or entrada[i].isdigit() or entrada[i] ==".":
                #3unavariable
                if entrada[i].isdigit() and temp =="" and digito=="":
                    digito = digito + entrada[i]
                if digito == "":
                    temp = temp + entrada[i]
                else:
                    if entrada[i].isdigit() or entrada[i]==".":
                        if digito!=entrada[i]:
                            digito = digito + entrada[i]
                    else:
                        temp = temp + entrada[i]
            else:
                insertarError(entrada[i],fila,columna)
        if estado == 1:
            if entrada[i]=="/" or entrada[i]=="*":
                contador = contador + 1

            if contador == 4:
                estado = 0
                contador = 0
                tokens = tokens + [[temp2, "tk_comentario", "Comentario creado por un usuario"] + [fila, columna]]
                temp2 = ""
            else:
                if entrada[i] != "/" and entrada[i] != "*":
                    temp2=temp2+entrada[i]
        if estado == 2:
            if entrada[i]=="\"":
                contador = contador + 1

            if contador == 2:
                estado = 0
                contador = 0
                tokens = tokens + [[temp2, "tk_cadena", "Valor tipo cadena"] + [fila, columna]]
                temp2=""
            else:
                if entrada[i]!="\"":
                    temp2 = temp2 + entrada[i]

    if temp != "" or digito != "":
        if temp == "false" or temp == "true":
            tokens = tokens + [[temp, "tk_booleano", "Valor reservado booleano"] + [fila, columna]]
            temp = ""
        elif temp != "":
            valor = insertarValor(temp, fila, columna)
            if valor[0] and insertadoInto==-1:
                insertadoInto = valor[1]
        if digito != "":
            tokens = tokens + [[digito, "tk_numerico", "Valor numerico asignado"] + [fila, columna]]
            digito = ""
    temp = ""
    digito = ""
    if imprimir:
        generarHtml()
    else:
        limpiarTokes()
    #print(tokens)
    #print(error)
    return tokens

def limpiarTokes():
    global tokens
    token_temp = []
    for i in range(len(tokens)):
        if tokens[i][1] != "tk_comentario":
            token_temp = token_temp + [tokens[i]]
    tokens = token_temp
def insertarValor(valor,fila,columna):
    global tokens
    posicion = -1
    insertado = True
    for i in range(len(reservado)):
        if reservado[i][0]==valor:
            tokens =tokens+ [reservado[i]+[fila,columna]]
            insertado = False

    if insertado:
        tokens = tokens + [[valor,"tk_idVariable","id de una variable"] + [fila, columna]]
        posicion = len(tokens)-1

    return insertado,posicion

def generarHtml():
    global tokens
    global error
    html_tokens = ""
    html_Error = ""
    html_tokens = "<html meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/><head><title>Componentes Encontrados</title>" \
                  "<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css\" integrity=\"sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z\" crossorigin=\"anonymous\"></head>" \
                  "</head>" \
                  "<body><center><h1>Componentes Encontrados</h1></center>" \
                  "<table class=\"table\"><thead class=\"thead-dark\">" \
                  "<tr>" \
                  "<th scope=\"col\">Componente</th>" \
                  "<th scope=\"col\">Tipo token</th>"\
                  "<th scope=\"col\">Descripción</th>" \
                  "<th scope=\"col\">Fila</th>" \
                  "<th scope=\"col\">Columna</th></tr>" \
                  "</thead><tbody><tr>"
    html_Error = "<html meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/><head><title>Errores</title>" \
                  "<link rel=\"stylesheet\" href=\"https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css\" integrity=\"sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z\" crossorigin=\"anonymous\"></head>" \
                  "</head>" \
                  "<body><center><h1>Componentes encontrados que no pertenecen</h1></center>" \
                  "<table class=\"table\"><thead class=\"thead-dark\">" \
                  "<tr>" \
                  "<th scope=\"col\">Componente</th>" \
                  "<th scope=\"col\">Tipo token</th>"\
                  "<th scope=\"col\">Descripción</th>" \
                  "<th scope=\"col\">Fila</th>" \
                  "<th scope=\"col\">Columna</th></tr>" \
                  "</thead><tbody><tr>"
    for i in range(len(tokens)):
        html_tokens = html_tokens + "<tr>"\
        "<td>" + str(tokens[i][0]) + "</td>" \
        "<td>" + str(tokens[i][1]) + "</td>" \
        "<td>" + str(tokens[i][2]) + "</td>" \
        "<td>" + str(tokens[i][3]) + "</td>" \
        "<td>" + str(tokens[i][4]) + "</td>" \
        "</tr>"

    for i in range(len(error)):
        html_Error = html_Error + "<tr>"\
        "<td>" + error[i][0] + "</td>" \
        "<td>" + error[i][1] + "</td>" \
        "<td>" + error[i][2] + "</td>" \
        "<td>" + str(error[i][3]) + "</td>" \
        "<td>" + str(error[i][4]) + "</td>" \
        "</tr>"

    html_tokens = html_tokens + "</tbody></table></body></html>"
    html_Error = html_Error + "</tbody></table></body></html>"
    try:
        file = open("componentes.html", "w")
        file.write(html_tokens)
        file.close()
        webbrowser.open_new_tab("componentes.html")
        file = open("error.html", "w")
        file.write(html_Error)
        file.close()
        webbrowser.open_new_tab("error.html")
        print("-> Operación Exitosa")
    except:
        print("-> No se ha podido completar esta acción")

def simboloPerteneciente(entrada,fila,columna):
    valor = False
    tokens = []
    for i in range(len(reservado)):
        if reservado[i][0]==entrada:
            tokens = [reservado[i]+[fila,columna]]
            valor = True
            break
    return valor, tokens


def insertarError(item,fila,columna):
    global error
    agregar = True
    if item == "\n":
        agregar = False
    if item == "	":
        agregar = False
    if item != "\n" and item != " ":
        if agregar:
            error = error + [[item, "tk_error", "Este item no pertenece al lenguaje", fila, columna]]

def prueba():
    manejo(txtPrueba,False)
#prueba()