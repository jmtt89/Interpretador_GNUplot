#! /usr/bin/env python

# Gabrielle Sparano 06-40358
# Jesus Torres 06-40386

import sys
import math
import re

# Lita de tokens del Lenguaje
tokens = (
    'NAME','NUMBER','FLOAT',
    'PLUS','MINUS','MULT','DIVIDE','EQUALS','POTENCIA',
    'PI','E',
    'SIN','COS','TAN','EXP','LOG','CEIL','FLOOR','RANGE',
    'WITH','PLOT','STILE',
    'LPAREN','RPAREN','COMEN','LCORCHT','RCORCHT','SEPAR','SEPARI',
    )

# Palabras Reservadas
reserved = {
    'pi'    : 'PI',
    'e'     : 'E',

    'sin'   : 'SIN',
    'cos'   : 'COS',
    'tan'   : 'TAN',
    'exp'   : 'EXP',
    'log'   : 'LOG',
    'ceil'  : 'CEIL',
    'floor' : 'FLOOR',

    'range' : 'RANGE',

    'plot'  : 'PLOT',
    'with'  : 'WITH',
    'stile' : 'STILE',

}

# Definicion de tokens simples


t_PLUS   = r'\+'
t_MINUS  = r'-'
t_MULT   = r'\*'
t_DIVIDE = r'/'
t_POTENCIA = r'\^'

t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCORCHT= r'\['
t_RCORCHT= r'\]'
t_SEPAR  = r','
t_SEPARI = r';'

# Definicion de tokens por Funciones
def t_STILE(t):
    r'linespoints|lines|points'
    t.type = 'STILE'
    return t

def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

def t_FLOAT(t):
    r'-?\d*\.\d*(e(-|\+)?\d+)?'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r' -?\d+ '
    t.value = int(t.value)
    return t

# Caracteres a ignorar
t_ignore = " \t\r"

# Comentario
def t_COMEN(t):
    r'(\#){1}[^\n]*'
    pass

# Nueva Linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Error
def t_error(t):
    print "Caracter Indefinido '"+str(t.value[0])+"' en Linea "+ str(t.lexer.lineno)+" en La Columna"+str(t.lexer.lexpos)
    t.lexer.skip(1)


# Contructor del Lexer
import lex
lex.lex()


# Parsing

precedence = (

    ('left','PLUS','MINUS'),
    ('left','MULT','DIVIDE','POTENCIA'),
    ('right','UMINUS'),
    )

# Diccionario de Nombres
names = { }

## ESTADO INICIAL
def p_statement_inst(p):
    'statement : listI'
    p[0]=p[1]

## Construcciones del Documento
def p_listI_normal(p):
    "listI  :   instruccion SEPARI listI"
    p[0] = p[1]+p[3]

def p_listI_comentario(p):
    "listI  :  COMEN listI"
    p[0] = p[2]

def p_listI_finnormal(p):
    "listI  :   instruccion "
    p[0] = p[1]

## EXPRESIONES
def p_expresion_var(p):
    "expresion  : NAME"
    p[0]=p[1]

def p_expresion_pi(p):
    "expresion : PI"
    p[0] = str(math.pi)

def p_expresion_e(p):
    "expresion : E"
    p[0] = str(math.e)

def p_expresion_number(p):
    "expresion : NUMBER"
    p[0]=str(p[1])
    
def p_expresion_float(p):
    "expresion : FLOAT"
    p[0]=str(p[1])

def p_expresion_binop(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion MULT expresion
                 | expresion DIVIDE expresion
                 | expresion POTENCIA expresion'''
    if p[2]=="^" :   p[0]="("+p[1]+"**"+p[3]+")"
    else :p[0]="("+p[1]+p[2]+p[3]+")"
    
def p_expresion_uminus(p):
    "expresion : MINUS expresion %prec UMINUS"
    p[0]=p[1]+p[2]

def p_fun(p):
    "expresion  : NAME LPAREN expresion RPAREN"
    try:
        if p[1] in names:
            p[0]=re.sub("(?<!\w)x(?!\w)",p[3],names[p[1]])
        else:
            raise e_nodef_fun(p[1],p.lineno(1),p.lexpos(3)-p.lexpos(1))
    except e_nodef_fun, S:
        sys.exit(S)
    

def p_expresion_fun(p):
    '''expresion : SIN LPAREN expresion RPAREN
                  | COS LPAREN expresion RPAREN
                  | TAN LPAREN expresion RPAREN
                  | EXP LPAREN expresion RPAREN
                  | LOG LPAREN expresion RPAREN
                  | CEIL LPAREN expresion RPAREN
                  | FLOOR LPAREN expresion RPAREN'''

    p[0]=p[1]+p[2]+p[3]+p[4]


def p_expresion_group(p):
    "expresion : LPAREN expresion RPAREN "
    p[0] = p[1]+p[2]+p[3]


## ARREGLOS

def p_array_arrvac(p):
    'array : LCORCHT RCORCHT'
    p[0] = []

def p_array_array(p):
    'array : LCORCHT items RCORCHT'
    p[0] = p[2]

def p_items(p):
    'items : expresion SEPAR items'
    p[0] = [p[1]]+p[3]

def p_items_ultimo(p):
    'items : expresion'
    p[0] = [p[1]]


##Evalua a Arreglo

def p_array_range(p):
    "rango  :   RANGE LPAREN expresion SEPAR expresion RPAREN "
    try:

        if not('x' in p[3]):
            if not('x' in p[5]):
                p[0] = "["+p[3]+":"+p[5]+"]"
            else:
                raise e_nonev_num(0,p.lineno(1),p.lexpos(5)-p.lexpos(1))
        else:
            raise e_nonev_num(0,p.lineno(1),p.lexpos(3)-p.lexpos(1))

    except e_nonev_num, S:
        sys.exit(S)


##INSTRUCCIONES

def p_instruccion_funcion(p):
    "instruccion    :   NAME LPAREN NAME RPAREN EQUALS expresion"
    l = re.findall("[a-zA-z]+",p[6])
    try:
        if p[1] in l:
            raise e_rec_call(p[1],p.lineno(1),p.lexpos(6)-p.lexpos(1))

        while p[3] in l:
                l.remove(p[3])

        while len(l)>0 and l[0] in reserved:
            l.remove(l[0])

        if not(len(l)==0):
            if re.search(l[0]+"(?=\()",p[6]):
                raise e_nodef_fun(l[0],p.lineno(1),p.lexpos(6)-p.lexpos(1))
            else:
                raise e_nodef_var(l[0],p.lineno(1),p.lexpos(6)-p.lexpos(1))

    except e_rec_call,A:
        sys.exit(A)
    except e_nodef_fun,B:
        sys.exit(B)
    except e_nodef_var,C:
        sys.exit(C)

    a = re.sub("(?<!\w)"+p[3]+"(?!\w)","x",p[6])
    names[p[1]]=a
    p[0]=""


def p_instruccion_plot(p):
    "instruccion   :    PLOT rango SEPAR expresion"
    l = re.findall("[a-zA-z]+",p[4])
    i=0
    while i<len(l):
        if l[i] in reserved:
            l.remove(l[i])
        else:
            i=i+1

    k=l[0]
    while k in l:
        l.remove(k)
    try:
        if len(l) > 0:
            raise e_nodef_var(l[0],p.lineno(1),p.lexpos(4)-p.lexpos(1))

        a = re.sub("(?<!\w)"+k+"(?!\w)",'x',p[4])

        p[0] = p[1]+" "+p[2]+" "+a

    except e_nodef_var,A:
        sys.exit(A)


def p_instruccion_plotWS(p):
    "instruccion   :   PLOT rango SEPAR expresion WITH STILE"
    l = re.findall("[a-zA-z]+",p[4])
    i=0
    while i<len(l):
        if l[i] in reserved:
            l.remove(l[i])
        else:
            i=i+1

    k=l[0]
    while k in l:
        l.remove(k)

    try:
        if len(l) > 0:
            raise e_nodef_var(l[0],p.lineno(1),p.lexpos(4)-p.lexpos(1))


        a = re.sub("(?<!\w)"+k+"(?!\w)",'x',p[4])
        p[0] = p[1]+" "+p[2]+" "+a+" "+p[5]+" "+p[6]

    except e_nodef_var,A:
        sys.exit(A)

    

def p_instruccion_plotWA(p):
    "instruccion   :    PLOT rango SEPAR array"
    i=0
    a=p[1]+" "+p[2]+" "
    b=""
    while(i<len(p[4])):
        if (i<len(p[4])-1): b = b+p[4][i]+","
        else : b = b+p[4][i]
        i=i+1

    l = re.findall("[a-zA-z]+",b)

    i=0
    while i<len(l):
        if l[i] in reserved:
            l.remove(l[i])
        else:
            i=i+1

    k=l[0]
    while k in l:
        l.remove(k)

    try:
        if len(l) > 0:
            raise e_nodef_var(l[0],p.lineno(1),p.lexpos(4)-p.lexpos(1))

        b = re.sub("(?<!\w)"+k+"(?!\w)",'x',b)
        p[0]=a+b

    except e_nodef_var,A:
        sys.exit(A)


def p_instruccion_plotWAS(p):
    "instruccion   :    PLOT rango SEPAR array WITH arrayS"
    try:
        if len(p[4])==len(p[6]):
            i=0
            a=p[1]+" "+p[2]+" "
            b=""
            while(i<len(p[4])):
                if (i<len(p[4])-1): b = b+p[4][i]+p[5]+" "+p[6][i]+","
                else : b = b+p[4][i]+p[5]+" "+p[6][i]
                i=i+1

            l = re.findall("[a-zA-z]+",b)

            i=0
            while i<len(l):
                if l[i] in reserved or l[i] in ['points','lines','linespoints']:
                    l.remove(l[i])
                else:
                    i=i+1

            k=l[0]
            while k in l:
                l.remove(k)


            if len(l) > 0:
                raise e_nodef_var(l[0],p.lineno(1),p.lexpos(4)-p.lexpos(1))


            b = re.sub("(?<!\w)"+k+"(?!\w)",'x',b)
            p[0]=a+b

        else:
            raise  e_incong_array(0,p.lineno(1),p.lexpos(4)-p.lexpos(1))
    except e_nodef_var,A:
        sys.exit(A)
    except  e_incong_array,B:
        sys.exit(B)



def p_solo_arrayS(p):
    "arrayS   :   LCORCHT STILE RCORCHT"
    p[0] = [str(p[2])]

def p_arrayS(p):
    "arrayS   :   LCORCHT STILE SEPAR itemS RCORCHT"
    p[0] = [str(p[2])]+p[4]

def p_itemS(p):
    'itemS : STILE SEPAR itemS'
    p[0]=[str(p[1])]+p[3]

def p_itemS_ultimo(p):
    'itemS : STILE'
    p[0] = [str(p[1])]
    

def p_error(p):
    if p:
        print("Error de Sintaxis '"+str(p.value)+"' en Linea "+str(p.lineno)+ " en Columna "+str(p.lexpos) )
    else:
        print("Error de sintaxis al Final del Archivo")

##Manejo de excepciones


class e_nodef_var(Exception): ## Variable no Permitida
    def __init__(self,valor,Lin,Col):
        self.valor=valor
        self.Lin=Lin
        self.Col=Col

    def __str__(self):
        return "Error variable libre "+str(self.valor)+" no permitida. En linea, "+str(self.Lin)+"; Columna "+str(self.Col)

class e_rec_call(Exception): ## LLamada Recursiva no permitida
    def __init__(self,valor,Lin,Col):
        self.valor=valor
        self.Lin=Lin
        self.Col=Col

    def __str__(self):
        return "Error En llamada Recursiva a Funcion "+str(self.valor)+". En linea, "+str(self.Lin)+"; Columna "+str(self.Col)

class e_nodef_fun(Exception): ## LLamada a Funcion no definida
    def __init__(self,valor,Lin,Col):
        self.valor=valor
        self.Lin=Lin
        self.Col=Col

    def __str__(self):
        return "Funcion "+str(self.valor)+" No definida. En linea, "+str(self.Lin)+"; Columna "+str(self.Col)

class e_incong_array(Exception): ##Error en los tamanos de arreglos de estilos y arreglo de expresiones graficables
    def __init__(self,valor,Lin,Col):
        self.valor=valor
        self.Lin=Lin
        self.Col=Col

    def __str__(self):
        return "Arreglo de Estilos y Arreglo de Expresiones Graficables de Tamanos Diferentes. En linea, "+str(self.Lin)+"; Columna "+str(self.Col)

class e_nonev_num(Exception): ## No evala a Numeros
    def __init__(self,valor,Lin,Col):
        self.valor=valor
        self.Lin=Lin
        self.Col=Col

    def __str__(self):
        return "La expresion del Range no evalua a Numeros. En linea, "+str(self.Lin)+"; Columna "+str(self.Col)

## Constructor del Parser
import yacc
yacc.yacc()

if __name__ == "__main__":

    NM = re.sub(".txt","",sys.argv[1])
    FIL = open(sys.argv[1],"r")

    a =yacc.parse(FIL.read(),tracking=True)

    NEW = open("entrada.pl","w")
    NEW.write("set term pdf\n")
    NEW.write("set output '"+NM+".pdf' \n")
    NEW.write(a)
    
