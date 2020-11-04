# Basilisk - Gramatica

Basilisk es una herramienta que se ayuda de autómatas (tanto finitos deterministas como con
pila) para validar scripts desarrollados en la versión ECMAScript o ES6 de javascript.

A continuación se desglosa la gramatica utilizada.

```
S -> ASIGNACION
    |IF
    |SWITCH
    |FOREACH
    |WHILE
    |LLAMADA_FUNCION
    |Λ

```
```
ASIGNACION -> TIPO_VARIABLE tk_idVariable = VALOR;


TIPO_VARIABLE -> var
                |let
                |const
                
                
                
VALOR -> tk_booleano
        |tk_digito
        |tk_cadena
        |FUNCION
    
    
FUNCION -> tk_idFuncion(LISTA_PARAMETRO){S}



LISTA_PARAMETRO -> PARAMETRO, LISTA_PARAMETRO
                  |PARAMETRO
                  

PARAMETRO -> VALOR
            |tk_idVariable
```
```
IF -> tk_if(VALOR_TIPO2){S}


VALOR_TIPO2 -> tk_idVariable
              |tk_booleano
```
```
WHILE -> tk_while(VALOR_TIPO2){S}
```
```
FOREACH -> tk_for(tk_idVariable in tk_idVariable){S}
```
```
SWITCH -> tk_switch(VALOR_TIPO2){CASE}
```
```

CASE  -> tk_case VALOR:S CASE;
        |tk_case VALOR:S;
        |tk_default:S CASE;
        |tk_break;
        
```
```
LLAMADA_FUNCION -> tk_idFUncion(LISTA_PARAMETRO){S}
```
### Simbolos no terminales

```
-S
-ASIGNACION
-IF
-SWITCH
-FOREACH
-WHILE
-LLAMADA_FUNCION
-TIPO_VARIABLE
-VALOR
-FUNCION
-PARAMETRO
-VALOR_TIPO2
-CASE
-LISTA_PARAMETRO

```

### Simbolos terminales
```
tk_booleano, tk_digito, tk_cadena, tk_idVariable, tk_idFuncion
tk_while, tk_for, tk_switch, tk_case
```
