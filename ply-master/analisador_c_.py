#!/usr/bin/env python3
import sys
import ply.lex as lex
import ply.yacc as yacc

# ---------- Análise Léxica ----------

tokens = (
    'TYPE', 'ID', 'NUMBER', 'CHAR',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'SEMICOLON', 'LPAREN', 'RPAREN'
)

t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_EQUALS    = r'='
t_SEMICOLON = r';'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

reserved = {'int':'TYPE', 'float':'TYPE', 'char':'TYPE'}

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+(\.\d+)?([eE][+-]?\d+)?'
    try:
        if '.' in t.value or 'e' in t.value.lower():
            t.value = float(t.value)
        else:
            t.value = int(t.value)
    except ValueError:
        print(f"Erro léxico: número inválido {t.value}")
        t.value = 0
    return t

def t_CHAR(t):
    r"'(\\.|[^\\'])'"
    t.value = t.value[1:-1]
    return t

# Ignora comentários

def t_COMMENT(t):
    r'//.*'
    pass

def t_COMMENT_BLOCK(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

# Ignorar espaços e tabs

t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Erro léxico: caractere inválido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ---------- Análise Sintática ----------

precedence = (
    ('right', 'UMINUS'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_assignment(p):
    'assignment : TYPE ID EQUALS expression SEMICOLON'
    p[0] = ('assign', p[1], p[2], p[4])
    print('Entrada válida. Árvore sintática:', p[0])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = ('binop', p[2], p[1], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_id(p):
    'expression : ID'
    p[0] = p[1]

def p_expression_char(p):
    'expression : CHAR'
    p[0] = p[1]

def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = ('uminus', p[2])

def p_error(p):
    if p:
        print(f"Erro sintático: token inesperado '{p.value}'")
    else:
        print("Erro sintático: fim de entrada inesperado")

parser = yacc.yacc()

def process_line(linha):
    # Exibe tokens reconhecidos
    print("\nTokens reconhecidos:")
    lexer.input(linha)
    for tok in lexer:
        print(f"  {tok.type:10} {tok.value!r}")
    # Análise sintática
    parser.parse(linha, lexer=lexer)
    print()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        process_line(' '.join(sys.argv[1:]))
    else:
        print("Analisador pronto. Digite 'exit' para sair.")
        while True:
            try:
                linha = input('> ')
            except EOFError:
                break
            if linha.lower() == 'exit':
                break
            process_line(linha)
