


import sys


# Lita de tokens del Lenguaje
tokens = (
    'NAME','NUMBER','FLOAT','FILE',
    'PLUS','MINUS','MULT','DIVIDE','EQUALS','POTENCIA',
    'MAYQ','MENQ','MAYI','MENI','EQUI','AND','OR','NOT',
    'PI','E',
    'SIN','COS','TAN','EXP','LOG','CIEL','FLOOR','RANGE','PUSH_BACK',
    'FOR','ENDFOR','STEP','IF','IN','WITH','PLOT','STILE',
    'LPAREN','RPAREN','COMEN','LCORCHT','RCORCHT','SEPAR','SEPARI',
    )

# Palabras Reservadas
reserved = {
    'pi'    : 'PI',
    'e'     : 'E',

    'and'   : 'AND',
    'or'    : 'OR',
    'not'   : 'NOT',

    'sin'   : 'SIN',
    'cos'   : 'COS',
    'tan'   : 'TAN',
    'exp'   : 'EXP',
    'log'   : 'LOG',
    'ciel'  : 'CIEL',
    'floor' : 'FLOOR',

    'range' : 'RANGE',
    'push_back' : 'PUSH_BACK',

    'for'   : 'FOR',
    'endfor': 'ENDFOR',
    'step'  : 'STEP',
    'if'    : 'IF',
    'in'    : 'IN',
    'plot'  : 'PLOT',
    'with'  : 'WITH',
    'stile' : 'STILE',

}

# Definicion de tokens simples

t_MAYQ  = r'>'
t_MENQ  = r'<'
t_MAYI  = r'>='
t_MENI  = r'<='
t_EQUI  = r'=='
t_AND   = r'and'
t_OR    = r'or'
t_NOT   = r'not'


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
t_FILE   = r'\'[a-zA-Z_][a-zA-Z0-9_]*\''

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
    r'(\+|-)?\d*\.\d*(e(-|\+)?\d+)?'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r' \d+ '
    t.value = int(t.value)
    return t

# Caracteres a ignorar
t_ignore = " \t\r"



## Comentario
def t_COMEN(t):
    r'(\#){1}[^\n]*'
    pass

# Nueva Linea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

# Error	
def t_error(t):
    print "Caracter Indefinido "+str(t.value[0])+" en Linea "+ str(t.lexer.lineno)
    t.lexer.skip(1)


# Contructor del Lexer
import lex
lex.lex()


# Parsing
precedence = (

    ('left','OR'),
    ('left','AND'),
    ('left','EQUI'),
    ('left','MAYQ','MENQ','MAYI','MENI'),
    ('left','PLUS','MINUS'),
    ('left','MULT','DIVIDE','POTENCIA'),
    ('right','UMINUS','NOT'),
    )

# Diccionario de Nombres (SIGUIENTE ENREGA)
names = { }

## ESTADO INICIAL
def p_statement_inst(p):
    'statement : listI'
    print(p[1])

## Construcciones del Documento	
def p_listI_normal(p):
    "listI  :   instruccion SEPARI listI"
    p[0] = str(p[1])+" \n"+str(p[3])+" \n"

def p_listI_confor(p):
    "listI  :   instruccionfor listI"
    p[0] = str(p[1])+" \n"+str(p[2])+" \n"

def p_listI_comentario(p):
    "listI  :  COMEN listI"
    p[0] = str(p[2])

def p_listI_finfor(p):
    "listI  :   instruccionfor "
    p[0] = str(p[1])

def p_listI_finnormal(p):
    "listI  :   instruccion "
    p[0] = str(p[1])

## EXPRESIONES
def p_var_name(p):
    "var :   NAME"
    p[0] = ('Expresion_Variable',p[1])

def p_expresion_var(p):
    "expresion :   NAME"
    p[0] = ('Expresion_Variable',p[1])

def p_expresion_pi(p):
    "expresion : PI"
    p[0] = ('Expresion_Constante',p[1])

def p_expresion_e(p):
    "expresion : E"
    p[0] = ('Expresion_Constante',p[1])

def p_expresion_number(p):
    "expresion : NUMBER"
    p[0] = ('Expresion_Numero_Entero',p[1])
    

def p_expresion_float(p):
    "expresion : FLOAT"
    p[0] = ('Expresion_Numero_Real',p[1])

def p_expresion_binop(p):
    '''expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion MULT expresion
                 | expresion DIVIDE expresion
                 | expresion POTENCIA expresion'''
    p[0] = ('Expresion_Binaria',p[2],p[1],p[3])
    

def p_expresion_uminus(p):
    "expresion : MINUS expresion %prec UMINUS"
    p[0] = ('Expresion_Unaria',p[2],p[1])


def p_expresion_fun(p):
    '''expresion : SIN LPAREN expresion RPAREN
                  | COS LPAREN expresion RPAREN
                  | TAN LPAREN expresion RPAREN
                  | EXP LPAREN expresion RPAREN
                  | LOG LPAREN expresion RPAREN
                  | CIEL LPAREN expresion RPAREN
                  | FLOOR LPAREN expresion RPAREN'''
    p[0] = ('FUN_Expresion',p[1],p[2])


def p_expresion_group(p):
    '''expresion : LPAREN expresion RPAREN '''
    p[0] = ('Expresion_Agrupamiento',p[2])


def p_expresion_if(p):
    "expresion    :   IF LPAREN condicion SEPAR expresion SEPAR expresion RPAREN"
    p[0] = ('Expresion_Condicional',p[3],p[5],p[7])


## CONDICIONES

def p_condicion_expresion(p):
    "condicion :  expresion"
    p[0] = ('Condicional',p[1])

def p_condicion_boolop(p):
    '''condicion : condicion MAYQ condicion
                 | condicion MENQ condicion
                 | condicion MAYI condicion
                 | condicion MENI condicion
                 | condicion EQUI condicion
                 | condicion AND condicion
                 | condicion OR condicion'''
    p[0] = ('Expresion_Binaria_Booleana',p[2],p[1],p[3])

def p_condicion_unaop(p):
    "condicion : NOT condicion "
    p[0] = ('Expresion_Unaria_Booleana',p[1],p[2])



## ARREGLOS

def p_array_arrvac(p):
    'expresion : LCORCHT RCORCHT'
    p[0] = ('Expresion_Arreglo_Vacio',p[1],p[2])

def p_array_array(p):
    'expresion : LCORCHT items RCORCHT'
    p[0] = ('Expresion_Arreglo',p[1],p[2],p[3])

def p_items(p):
    'items : expresion SEPAR items'
    p[0] = (p[1],p[3])


def p_items_ultimo(p):
    'items : expresion'
    p[0] = (p[1])

def p_array_range(p):
    "expresion  :   RANGE LPAREN expresion SEPAR expresion RPAREN "
    p[0] = ('FUNCION_RANGO',p[3],p[5])

def p_array_arrcomp(p):
    "expresion  :   LCORCHT expresion FOR var IN expresion RCORCHT"
    p[0] = ('Arreglo_Compresion',p[2],p[4],p[6])


##INSTRUCCIONES

def p_instruccion_funcion(p):
    "instruccion    :   NAME LPAREN var RPAREN EQUALS expresion"
    p[0] = ('Declaracion_Funcion',p[1],p[3],p[6])


def p_instruccion_asinacion(p):
    "instruccion    :   var EQUALS expresion"
    p[0] = ('Asignacion_Variable',p[1],p[3])


def p_instruccion_plot(p):
    "instruccion   :    PLOT expresion SEPAR dude"
    p[0] = ('GRAFICAR',p[2],p[4])

def p_instruccion_plotWS(p):
    "instruccion   :   PLOT expresion SEPAR dude WITH STILE"
    p[0] = ('GRAFICAR',p[2],p[4],p[6])
    
def p_instruccion_plotWAS(p):
    "instruccion   :    PLOT expresion SEPAR dude WITH arrayS"
    p[0] = ('GRAFICAR',p[2],p[4],p[6])


def p_dude_instruccion(p):
    '''dude   :     expresion
              |     file'''
    p[0]=p[1]

def p_file(p):
    "file   : FILE"
    p[0] = ('Expresion_Graficable',p[1])

def p_arrayS(p):
    "arrayS   :   LCORCHT itemS RCORCHT"
    p[0] = ('Arreglo_Stilos',p[2])

def p_itemS(p):
    'itemS : STILE SEPAR itemS'
    p[0] = (str(p[1]),p[3])

def p_itemS_ultimo(p):
    'itemS : STILE'
    p[0] = str(p[1])

def p_instruccion_push(p):
    "instruccion  : PUSH_BACK LPAREN var SEPAR expresion RPAREN"
    p[0] = ('Push_back',p[3],p[5])

def p_instruccionfor_for(p):
    "instruccionfor    :   FOR var IN expresion listI ENDFOR"
    p[0] = ('CICLO',p[2],p[4],p[5])

def p_instruccionfor_forWS(p):
    "instruccionfor    :   FOR var IN expresion STEP expresion listI ENDFOR"
    p[0] = ('CICLO',p[2],p[4],p[6],p[7])
    

def p_error(p):
    if p:
        print("Error de Sintaxis "+str(p.value)+" en Linea "+str(p.lineno)+ "en Columna "+str(p.lexpos) )
    else:
        print("Error de sintaxis al Final del Archivo")


## Constructor del Parser
import yacc
yacc.yacc()

if __name__ == "__main__":

    FIL = open(sys.argv[1],"r")

    yacc.parse(FIL.read(),tracking=True)
    
