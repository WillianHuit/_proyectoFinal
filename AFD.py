#"if" - tk_if - palabra reservada if - fila:5 - columna:10
#tk_{ tk_} tk_( tk_) tk_true tk_false
import webbrowser
txtPrueba = "funcion1(4, true, variable1);"


reservado = [["let","tk_variable","palabra reservada variable"],["var","tk_variable","palabra reservada variable"],
             ["const","tk_variable","palabra reservada variable"],["if","tk_if","palabra reservada if"],
             ["while","tk_while","Palabra reservada while"],["foreach","tk_for","Palabra reservada for"],
             ["switch","tk_switch","Palabra reservada switch"],
             ["(","tk_parentesis","parentesis de apertura"],[")","tk_parentesis","parentesis de cierre"],["{","tk_corchete","corchete de apertura"],
             ["}","tk_corchete","corchete de cierre"],[";","tk_Comillas","Simbolo delimitador"],
             ["=>","tk_flecha","Simbolo flecha"],["=","tk_igualdad","Simbolo de igualdad"]]
tokens = []
error = []

def manejo(entrada):
    global tokens
    global error
    digitos = ""
    fila = 1
    columna = 0
    estado = 0
    temp = ""
    funcion = ""
    comentarioCount = 0
    cadenaCount = 0
    switchCount = 0
    caseCount = False
    for i in range(len(entrada)):
        columna = columna + 1
        if estado == 0:

            if entrada[i].isalpha():
                temp = temp + entrada[i]
                funcion = funcion + entrada[i]
            elif entrada[i].isdigit():
                funcion = funcion + entrada[i]
            elif entrada[i] == " " or entrada[i]=="(":
                if temp!="" and temp!="defalut" and temp!="case":
                    estado = 1
            elif entrada[i] == "/":
                comentarioCount = 0
                estado = 2
            elif entrada[i]=="}":
                tokens = tokens + [["}","tk_corchete","corchete de cierre"]+[ fila, columna]]
                if caseCount:
                    caseCount = False
            elif temp == "case" or temp == "default":
                if caseCount:
                    estado = 13
            elif temp == "break":
                if caseCount:
                    tokens = tokens + [[temp, "tk_break", "delimita el caso"] + [fila, columna]]
                    if entrada[i] == ";":
                        tokens = tokens + [[";", "tk_delimitador", "Simbolo delimitador"] + [fila, columna]]
                    temp = ""
            else:
                if entrada[i]!=" ":
                    insertarError(entrada[i], fila, columna)
        if estado == 1:
            guia = -1
            for j in range(len(reservado)):
                if temp == reservado[j][0]:
                    tokens = tokens + [reservado[j]+[fila,columna]]
                    guia = j
                    break
            if guia == -1:
                if entrada[i]=="(":
                    estado = 15
                    tokens = tokens + [[funcion, "tk_funcion", "llamada de una función"] + [fila, columna]]
                    funcion = ""
                else:
                    insertarError(temp, fila, columna)
                    estado = 0

            elif guia>=0 and guia <= 2:
                estado = 3
            elif guia>2 and guia<6:
                estado = 9
            elif guia == 6:
                estado = 11
            #5
            temp = ""
        #Este es el estado de comentarios
        if estado == 2:
            if entrada[i] == "/":
                comentarioCount = comentarioCount + 1
            elif entrada[i] == "*":
                comentarioCount = comentarioCount + 1
            else:
                temp = temp + entrada[i]
            if comentarioCount == 4:
                tokens = tokens + [[temp,"tk_comentario","Comentario realizado por el usuario",fila,columna]]
                temp =""
                estado = 0
                comentarioCount = 0
        #Estados de variables
        if estado == 3:
            if entrada[i] == "_" or entrada[i].isalpha() or entrada[i].isdigit():
                temp = temp + entrada[i]
            elif entrada[i] == "=" or entrada[i]==" ":
                if temp != "":
                    tokens = tokens + [[temp, "tk_idVariable", "Nombre asignado a una variable",fila,columna]]
                    temp = ""
                    cadenaCount = 0
                    estado = 4
            else:
                insertarError(entrada[i],fila,columna)
        if estado == 4:
            if entrada[i] == "=":
                tokens = tokens + [["=","tk_igualdad","Simbolo de igualdad",fila,columna]]
            elif entrada[i] == "\"":
                estado = 5
            elif entrada[i] == ";":
                if cadenaCount > 1:
                    tokens = tokens + [[temp, "tk_cadena", "cadena ingresada a una variable",fila,columna]]
                else:
                    if temp == "true" or temp == "false":
                        tokens = tokens + [[temp, "tk_bool", "valor booleano ingresado a una variable",fila,columna]]
                    else:
                        if digitos.isdigit():
                            tokens = tokens + [[temp, "tk_digit", "valor numerico ingresado a una variable",fila,columna]]
                        else:
                            insertarError(temp, fila, columna)
                tokens = tokens + [[";","tk_delimitador","simbolo delimitador",fila,columna]]
                temp = ""
                digitos = ""
                estado = 0
            elif entrada[i]=="(":
                tokens = tokens + [["(","tk_parentesis","parentesis de apertura",fila,columna]]
                temp = ""
                estado = 6
            elif entrada[i] == "." or entrada[i].isalpha() or entrada[i].isdigit():
                temp = temp + entrada[i]
                if entrada[i].isalpha() or entrada[i].isdigit():
                    digitos = digitos + entrada[i]
            else:
                if entrada[i]!=" ":
                    insertarError(entrada[i], fila, columna)
        if estado == 5:
            cadenaCount = cadenaCount + 1
            if entrada[i]=="\"" and cadenaCount > 1:
                estado = 4
            else:
                if entrada[i]!="\"":
                    temp = temp + entrada[i]
        #Declaración de funciones
        if estado == 6:
            if entrada[i]==")":
                tokens = tokens + [[temp, "tk_parametro", "Parametro asigando a una función",fila,columna]]
                tokens = tokens + [[")","tk_parentesis","parentesis de cierre",fila,columna]]
                temp = ""
                estado = 7
            elif entrada[i].isalpha() or entrada[i].isdigit() or entrada[i]==" ":
                temp = temp + entrada[i]
            elif entrada[i] == ",":
                tokens = tokens + [[temp, "tk_parametro","Parametro asigando a una función",fila,columna]]
                temp = ""
            else:
                if entrada[i] != "(" and entrada[i]!=" ":
                    insertarError(entrada[i], fila, columna)
        if estado == 7:
            if entrada[i] ==">" and entrada[i-1]=="=":
                estado = 8
        if estado == 8:
            if entrada[i]=="{":
                tokens = tokens + [["{","tk_corchete","corchete de apertura",fila,columna]]
                estado = 0
        #Estado salto de linea
        if estado == 9:
            if entrada[i]=="(":
                tokens = tokens + [["(","tk_parentesis","parentesis de apertura", fila, columna]]
            elif entrada[i].isalpha() or entrada[i].isdigit() or entrada[i]==" ":
                temp = temp + entrada[i]
            elif entrada[i] == ")":
                if temp == "true":
                    tokens = tokens + [[temp, "tk_bool", "valor booleano ingresado a una sentencia", fila, columna]]
                elif temp == "false":
                    tokens = tokens + [[temp, "tk_bool", "valor booleano ingresado a una sentencia", fila, columna]]
                else:
                    tokens = tokens + [[temp, "tk_identificador", "identificador de una sentencia", fila, columna]]
                estado = 10
                temp = ""
            else:
                if entrada[i] != " ":
                    insertarError(entrada[i],fila,columna)
        if estado == 10:
            if entrada[i] == ")":
                tokens = tokens + [[")","tk_parentesis","parentesis de cierre",fila,columna]]
            elif entrada[i] == "{":
                tokens = tokens + [["{","tk_corchete","corchete de apertura",fila,columna]]
                estado = 0
            else:
                if entrada[i] != " ":
                    insertarError(entrada[i],fila,columna)
        if estado == 11:
            if entrada[i]=="(":
                tokens = tokens + [["(","tk_parentesis","parentesis de apertura", fila, columna]]
            elif entrada[i].isalpha() or entrada[i].isdigit():
                temp = temp + entrada[i]
            elif entrada[i] == ")":
                if temp == "true":
                    tokens = tokens + [[temp, "tk_bool", "valor booleano ingresado a una sentencia", fila, columna]]
                elif temp == "false":
                    tokens = tokens + [[temp, "tk_bool", "valor booleano ingresado a una sentencia", fila, columna]]
                else:
                    tokens = tokens + [[temp, "tk_identificador", "identificador de una sentencia", fila, columna]]
                estado = 12
                temp = ""
            else:
                if entrada[i] != " ":
                    insertarError(entrada[i],fila,columna)
        if estado == 12:
            if entrada[i] == ")":
                tokens = tokens + [[")", "tk_parentesis", "parentesis de cierre", fila, columna]]
            elif entrada[i] == "{":
                tokens = tokens + [["{", "tk_corchete", "corchete de apertura", fila, columna]]
                estado = 13
                caseCount = True
                temp = ""
            else:
                if entrada[i] != " ":
                    insertarError(entrada[i], fila, columna)
        if estado == 13:
            funcion = ""
            if temp == "case" and caseCount:
                tokens = tokens + [["case", "tk_case", "Opcion case", fila, columna]]
                temp = ""
                estado = 14
            elif temp == "default" and caseCount:
                if entrada[i]==":":
                    tokens = tokens + [["default", "tk_case", "Opcion case", fila, columna]]
                    tokens = tokens + [[":", "tk_dosPuntos", "indica la acción del case", fila, columna]]
                    temp = ""
                    estado = 0
            elif entrada[i].isalpha():
                temp = temp + entrada[i]
            else:
                if entrada[i]!=" " and entrada[i]!="{":
                    insertarError(entrada[i],fila,columna)
        if estado == 14:
            if entrada[i] == "\"":
                comentarioCount = comentarioCount + 1
            if comentarioCount > 0 and entrada[i]!="\"":
                temp = temp + entrada[i]
            elif entrada[i].isalpha() or entrada[i].isdigit() or entrada[i]==".":
                temp = temp + entrada[i]
                if entrada[i]!=".":
                    digitos = digitos + entrada[i]
            elif entrada[i]==":":
                if comentarioCount == 2:
                    tokens = tokens + [[temp, "tk_cadena", "condicion cadena en case", fila, columna]]
                elif digitos.isdigit():
                    tokens = tokens + [[temp, "tk_digito", "condicion numerica en case", fila, columna]]
                else:
                    tokens = tokens + [[temp, "tk_bool", "condicion booleana en case", fila, columna]]
                tokens = tokens + [[":", "tk_dosPuntos", "indica la acción del case", fila, columna]]
                estado = 0
                temp = ""
                digitos = ""
                comentarioCount = 0
        if estado == 15:
            if entrada[i] == "(":
                tokens = tokens + [["(", "tk_parentesis", "parentesis de apertura", fila, columna]]
            elif entrada[i]=="\"":
                cadenaCount = cadenaCount + 1
            elif entrada[i].isalpha() or entrada[i].isdigit() or entrada[i] == "." or entrada[i]==" ":
                if entrada[i]==" " and cadenaCount>=1:
                    temp = temp + entrada[i]
                elif entrada[i]!=" ":
                    if entrada[i]!=".":
                        digitos = digitos + entrada[i]
                    temp = temp + entrada[i]
            elif entrada[i]==",":
                if cadenaCount > 1:
                    tokens = tokens + [[temp, "tk_cadena", "parametro tipo cadena", fila, columna]]
                elif digitos.isdigit():
                    tokens = tokens + [[temp, "tk_digito", "parametro tipo digito", fila, columna]]
                elif temp=="true" or temp=="false":
                    tokens = tokens + [[temp, "tk_bool", "parametro tipo booleano", fila, columna]]
                else:
                    tokens = tokens + [[temp, "tk_variable", "parametro tipo variable", fila, columna]]
                temp = ""
            elif entrada[i]==")":
                if cadenaCount > 1:
                    tokens = tokens + [[temp, "tk_cadena", "parametro tipo cadena", fila, columna]]
                elif digitos.isdigit():
                    tokens = tokens + [[temp, "tk_digito", "parametro tipo digito", fila, columna]]
                elif temp=="true" or temp=="false":
                    tokens = tokens + [[temp, "tk_bool", "parametro tipo booleano", fila, columna]]
                else:
                    tokens = tokens + [[temp, "tk_variable", "parametro tipo variable", fila, columna]]
                tokens = tokens + [[entrada[i], "tk_parentesis", "parentesis de cierre", fila, columna]]

                temp = ""
                digitos = ""
                cadenaCount = 0
            elif entrada[i]==";":
                tokens = tokens + [[entrada[i], "tk_delimitador", "simbolo delimitador", fila, columna]]
                estado = 0


        if entrada[i] =="\n":
            fila = fila + 1
            columna = 0


    generarHtml()

def generarHtml():
    global tokens
    global error
    print(tokens)
    print(error)
    html_tokens = ""
    html_Error = ""
    html_tokens = "<html<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/><head><title>Componentes Encontrados</title>" \
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
    html_Error = "<html<meta http-equiv=\"Content-Type\" content=\"text/html; charset=UTF-8\"/><head><title>Errores</title>" \
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
    for i in range(len(tokens)-10):
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

def insertarError(item,fila,columna):
    global error
    agregar = True
    if item == "\n":
        agregar = False
    if item == "	":
        agregar = False
    if item != "\n" or item != " ":
        if agregar:
            error = error + [[item, "tk_error", "Este item no pertenece al lenguaje", fila, columna]]

#manejo(txtPrueba)