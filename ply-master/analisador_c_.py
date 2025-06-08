#!/usr/bin/env python3
import sys
import ply.lex as lex
import ply.yacc as yacc

# -----------------------------------------------------------------------------
# 1) Declaração de tokens e palavras-reservadas

tokens = (
    'IF', 'ELSE', 'SWITCH', 'CASE', 'DEFAULT', 'BREAK',  # controle
    'WHILE', 'FOR',                                       # repetição
    'TYPE',                                              # tipos
    'ID', 'NUMBER', 'CHAR_LITERAL', 'STRING_LITERAL',    # literais
    'EQ', 'NE', 'LT', 'LE', 'GT', 'GE',                  # relacionais
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',                  # aritméticos
    'PLUSEQ', 'MINUSEQ', 'TIMESEQ', 'DIVEQ', 'EQUALS',  # atribuição
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COLON', 'COMMA', 'SEMICOLON',
)
reserved = {
    'if': 'IF', 'else': 'ELSE', 'switch': 'SWITCH', 'case': 'CASE',
    'default': 'DEFAULT', 'break': 'BREAK', 'while': 'WHILE', 'for': 'FOR',
    'int': 'TYPE', 'float': 'TYPE', 'char': 'TYPE',
}

# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# -----------------------------------------------------------------------------
# 2) Expressões regulares para tokens básicos

# Pontuação
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_COLON     = r':'
t_COMMA     = r','
t_SEMICOLON = r';'

# Operadores relacionais (definidos como funções para precedência)
def t_EQ(t):
    r'=='
    return t
def t_NE(t):
    r'!='
    return t
def t_LE(t):
    r'<='
    return t
def t_GE(t):
    r'>='
    return t
def t_LT(t):
    r'<' 
    return t
def t_GT(t):
    r'>'
    return t

# Operadores de atribuição composta
def t_PLUSEQ(t):
    r'\+='  
    return t
def t_MINUSEQ(t):
    r'-='  
    return t
def t_TIMESEQ(t):
    r'\*='  
    return t
def t_DIVEQ(t):
    r'/='  
    return t

# Operador de atribuição simples
def t_EQUALS(t):
    r'='  
    return t

# Operadores aritméticos
def t_PLUS(t):
    r'\+'  
    return t
def t_MINUS(t):
    r'-'  
    return t
def t_TIMES(t):
    r'\*'  
    return t
def t_DIVIDE(t):
    r'/'  
    return t

# Literais
t_CHAR_LITERAL   = r"'(\.|[^\'])'"
t_STRING_LITERAL = r'"(\.|[^\"])*"'

# -----------------------------------------------------------------------------
# 3) Identificador e palavras-reservadas

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# -----------------------------------------------------------------------------
# 4) Número inteiro ou ponto-flutuante

def t_NUMBER(t):
    r'\d+(?:\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

# -----------------------------------------------------------------------------
# 5) Comentários

def t_COMMENT(t):
    r'//.*'
    pass

def t_COMMENT_BLOCK(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

# -----------------------------------------------------------------------------
# 6) Ignorar espaços e tabs

t_ignore = ' \t\r\n'

def t_error(t):
    print(f"Erro léxico: caractere inválido '{t.value[0]}' (linha {t.lineno})")
    t.lexer.skip(1)

lexer = lex.lex()

# -----------------------------------------------------------------------------
# 7) Precedência de operadores

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# -----------------------------------------------------------------------------
# 8) Início da gramática

start = 'program'

# -----------------------------------------------------------------------------
# 9) Produções sintáticas básicas

def p_program(p):
    'program : stmt_list'
    p[0] = p[1]

def p_stmt_list(p):
    'stmt_list : stmt stmt_list'
    p[0] = [p[1]] + p[2]

def p_stmt_list_empty(p):
    'stmt_list : empty'
    p[0] = []

def p_empty(p):
    'empty :'
    p[0] = []

# qualquer comando válido

def p_stmt(p):
    '''stmt : var_decl
             | assign_stmt
             | if_stmt
             | switch_stmt
             | while_stmt
             | for_stmt
             | break_stmt'''
    p[0] = p[1]

# declaração de variáveis

def p_var_decl(p):
    'var_decl : TYPE declarator_list SEMICOLON'
    p[0] = ('decl', p[1], p[2])

def p_declarator_list_single(p):
    'declarator_list : declarator'
    p[0] = [p[1]]

def p_declarator_list_multi(p):
    'declarator_list : declarator_list COMMA declarator'
    p[0] = p[1] + [p[3]]

def p_declarator_no_init(p):
    'declarator : ID'
    p[0] = ('var', p[1], None)

def p_declarator_init(p):
    'declarator : ID EQUALS initializer'
    p[0] = ('var', p[1], p[3])

def p_initializer_number(p):
    'initializer : NUMBER'
    p[0] = p[1]

def p_initializer_char(p):
    'initializer : CHAR_LITERAL'
    p[0] = p[1]

def p_initializer_string(p):
    'initializer : STRING_LITERAL'
    p[0] = p[1]

# atribuição

def p_assign_stmt(p):
    'assign_stmt : ID assign_op expr SEMICOLON'
    p[0] = ('assign', p[1], p[2], p[3])

def p_assign_op(p):
    '''assign_op : EQUALS
                  | PLUSEQ
                  | MINUSEQ
                  | TIMESEQ
                  | DIVEQ'''
    p[0] = p[1]

# expressões aritméticas

def p_expr_plus(p):
    'expr : expr PLUS term'
    p[0] = ('+', p[1], p[3])

def p_expr_minus(p):
    'expr : expr MINUS term'
    p[0] = ('-', p[1], p[3])

def p_expr_term(p):
    'expr : term'
    p[0] = p[1]

def p_term_times(p):
    'term : term TIMES factor'
    p[0] = ('*', p[1], p[3])

def p_term_div(p):
    'term : term DIVIDE factor'
    p[0] = ('/', p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_id(p):
    'factor : ID'
    p[0] = ('id', p[1])

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = ('num', p[1])

def p_factor_paren(p):
    'factor : LPAREN expr RPAREN'
    p[0] = p[2]

# condição relacional

def p_cond(p):
    'cond : expr relop expr'
    p[0] = ('cond', p[2], p[1], p[3])

def p_relop(p):
    '''relop : EQ
             | NE
             | LT
             | LE
             | GT
             | GE'''
    p[0] = p[1]

# if / else

def p_if_stmt(p):
    'if_stmt : IF LPAREN cond RPAREN compound_stmt opt_else'
    p[0] = ('if', p[3], p[5], p[6])

def p_opt_else(p):
    '''opt_else : ELSE compound_stmt
                | empty'''
    p[0] = p[2] if len(p) == 3 else None

# switch / case

def p_switch_stmt(p):
    'switch_stmt : SWITCH LPAREN ID RPAREN LBRACE case_block_list opt_default RBRACE'
    p[0] = ('switch', p[3], p[6], p[7])

def p_case_block_list(p):
    '''case_block_list : case_block case_block_list
                       | empty'''
    p[0] = [p[1]] + p[2] if len(p) == 3 else []

def p_case_block(p):
    'case_block : case_label_list compound_stmt'
    p[0] = ('case', p[1], p[2])

def p_case_label_list_single(p):
    'case_label_list : CASE ID COLON'
    p[0] = [p[2]]

def p_case_label_list_multi(p):
    'case_label_list : CASE ID COLON case_label_list'
    p[0] = [p[2]] + p[4]

def p_opt_default(p):
    '''opt_default : DEFAULT COLON compound_stmt
                   | empty'''
    p[0] = ('default', p[3]) if len(p) == 4 else None

# while

def p_while_stmt(p):
    'while_stmt : WHILE LPAREN cond RPAREN compound_stmt'
    p[0] = ('while', p[3], p[5])

# for

def p_initializer_for(p):
    'initializer_for : ID assign_op expr'
    p[0] = ('init', p[1], p[2], p[3])

def p_iteration(p):
    'iteration : ID assign_op expr'
    p[0] = ('iter', p[1], p[2], p[3])

def p_for_stmt(p):
    'for_stmt : FOR LPAREN initializer_for SEMICOLON cond SEMICOLON iteration RPAREN compound_stmt'
    p[0] = ('for', p[3], p[5], p[7], p[9])

# bloco composto

def p_compound_stmt(p):
    'compound_stmt : LBRACE stmt_list RBRACE'
    p[0] = ('block', p[2])

# break

def p_break_stmt(p):
    'break_stmt : BREAK SEMICOLON'
    p[0] = ('break',)

# erros sintáticos

def p_error(p):
    if p:
        print(f"Erro sintático: token inesperado '{p.value}' (linha {p.lineno})")
    else:
        print("Erro sintático: fim de entrada inesperado")

# construir parser
parser = yacc.yacc()

# -----------------------------------------------------------------------------
# 10) Processamento de entrada

def process_input(text):
    print("\nTokens reconhecidos:")
    lexer.input(text)
    for tok in lexer:
        print(f"  {tok.type:12} {tok.value!r}")
    try:
        ast = parser.parse(text, lexer=lexer)
        print("Árvore sintática (AST):", ast)
    except Exception:
        pass

# -----------------------------------------------------------------------------
# 11) Modo interativo e leitura de arquivo com buffering

def main():
    if len(sys.argv) == 1:
        print("Analisador pronto. Digite 'exit' para sair.")
        buffer = ""
        brace_balance = 0
        while True:
            try:
                prompt = '> ' if not buffer else '... '
                line = input(prompt)
            except EOFError:
                break
            if line.lower() == 'exit':
                break

            buffer += line + '\n'
            brace_balance += line.count('{') - line.count('}')

            if brace_balance == 0 and buffer.strip():
                process_input(buffer)
                buffer = ""
                brace_balance = 0

    elif len(sys.argv) == 2 and sys.argv[1].endswith('.txt'):
        arquivo = sys.argv[1]
        try:
            buffer = ""
            brace_balance = 0
            skip_block = False
            with open(arquivo, 'r', encoding='utf-8') as f:
                for line in f:
                    stripped_line = line.strip()
                    # Skip single-line comments
                    if not skip_block and stripped_line.startswith('//'):
                        continue
                    # Handle start of block comment
                    if '/*' in stripped_line:
                        skip_block = True
                        # If end of block comment on same line, end skip
                        if '*/' in stripped_line:
                            skip_block = False
                        continue
                    # Handle end of block comment
                    if skip_block:
                        if '*/' in stripped_line:
                            skip_block = False
                        continue
                    # Add line if not skipping
                    buffer += line
                    brace_balance += line.count('{') - line.count('}')
                    if brace_balance == 0 and buffer.strip():
                        process_input(buffer)
                        buffer = ""
            # Process any remaining buffer
            if buffer.strip():
                process_input(buffer)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {arquivo}")
    elif len(sys.argv) == 2:
        process_input(sys.argv[1])

    else:
        print("Uso: python analisador_c_.py [arquivo.txt | \"decl\" ]")
        sys.exit(1)

if __name__ == '__main__':
    main()
