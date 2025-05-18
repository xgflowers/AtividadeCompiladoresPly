'''
Analisador Léxico e Sintático para atribuições simples em C
Ferramenta: PLY (Python Lex-Yacc)

Requisitos:
    pip install ply

Como executar:
    python analisador_c_assignment.py

No prompt, digite uma linha de atribuição C (ex: int x = 10 + y;) e pressione Enter.
Para sair, digite "exit".

Exemplos válidos:
    int a = 5;
    float z = 3.14 * r;
    char c = 'x';

Exemplos inválidos:
    int = 5;
    float 2x = 3.0;
    int x 5;
'''
import ply.lex as lex
import ply.yacc as yacc

# ---------- Análise Léxica ----------

# Lista de tokens
tokens = (
    'TYPE', 'ID', 'NUMBER', 'CHAR',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'EQUALS', 'SEMICOLON', 'LPAREN', 'RPAREN'
)

# Definições de tokens simples
t_PLUS      = r'\+'
t_MINUS     = r'-'
t_TIMES     = r'\*'
t_DIVIDE    = r'/'
t_EQUALS    = r'='
t_SEMICOLON = r';'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

# Palavras reservadas e tipos básicos
reserved = {
    'int': 'TYPE',
    'float': 'TYPE',
    'char': 'TYPE'
}

# Identificadores e reserva
def t_ID(t):
    r"[a-zA-Z_][a-zA-Z0-9_]*"
    t.type = reserved.get(t.value, 'ID')
    return t

# Números (inteiros e floats)
def t_NUMBER(t):
    r"\d+(\.\d+)?"
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# Caracteres simples

def t_CHAR(t):
    r"'(.|\\n)'"
    t.value = t.value[1:-1]
    return t

# Ignorar espaços e tabs
t_ignore = ' \t'

# Quebra de linha
 def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

# Erro léxico
def t_error(t):
    print(f"Erro léxico: caractere inválido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ---------- Análise Sintática ----------

# Precedência de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Regra principal de atribuição
 def p_assignment(p):
    'assignment : TYPE ID EQUALS expression SEMICOLON'
    p[0] = ('assign', p[1], p[2], p[4])
    print('Entrada válida. Árvore sintática:', p[0])

# Expressões binárias
 def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression.DIVIDE expression'''
    p[0] = ('binop', p[2], p[1], p[3])

# Parênteses em expressões
 def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

# Número isolado
 def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

# Identificador isolado
 def p_expression_id(p):
    'expression : ID'
    p[0] = p[1]

# Erro sintático
 def p_error(p):
    if p:
        print(f"Erro sintático: token inesperado '{p.value}'")
    else:
        print("Erro sintático: fim de entrada inesperado")

parser = yacc.yacc()

# Loop interativo
if __name__ == '__main__':
    print("Analisador pronto. Digite 'exit' para sair.")
    while True:
        try:
            linha = input('> ')
        except EOFError:
            break
        if linha.lower() == 'exit':
            break
        parser.parse(linha)
