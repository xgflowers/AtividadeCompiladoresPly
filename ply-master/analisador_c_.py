#!/usr/bin/env python3
import sys
import ply.lex as lex
import ply.yacc as yacc

# -----------------------------------------------------------------------------
# 1) Declaração de tokens e palavras-reservadas

tokens = (
    # Palavras-reservadas de seleção
    'IF', 'ELSE', 'SWITCH', 'CASE', 'DEFAULT', 'BREAK',
    # Tipos (reservadas para declaração de variáveis)
    'TYPE',
    # Literais e identificadores
    'ID', 'NUMBER', 'CHAR_LITERAL', 'STRING_LITERAL',
    # Operadores relacionais
    'EQ',   # ==
    'NE',   # !=
    'LT',   # <
    'LE',   # <=
    'GT',   # >
    'GE',   # >=
    # Operadores aritméticos e de atribuição composta
    'PLUS',     # +
    'MINUS',    # -
    'TIMES',    # *
    'DIVIDE',   # /
    'PLUSEQ',   # +=
    'MINUSEQ',  # -=
    'TIMESEQ',  # *=
    'DIVEQ',    # /=
    'EQUALS',   # =   (atribuição simples)
    # Pontuação
    'LPAREN',   # (
    'RPAREN',   # )
    'LBRACE',   # {
    'RBRACE',   # }
    'COLON',    # :
    'COMMA',    # ,
    'SEMICOLON',# ;
)

reserved = {
    'if':      'IF',
    'else':    'ELSE',
    'switch':  'SWITCH',
    'case':    'CASE',
    'default': 'DEFAULT',
    'break':   'BREAK',
    'int':     'TYPE',
    'float':   'TYPE',
    'char':    'TYPE',
}

# -----------------------------------------------------------------------------
# 2) Expressões regulares para tokens “literais” (parênteses, chaves, etc.)

t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LBRACE    = r'\{'
t_RBRACE    = r'\}'
t_COLON     = r':'
t_COMMA     = r','
t_SEMICOLON = r';'

# -----------------------------------------------------------------------------
# 3) Operadores relacionais (sempre listar maiores antes dos menores)

t_EQ  = r'=='
t_NE  = r'!='
t_LE  = r'<='
t_GE  = r'>='
t_LT  = r'<'
t_GT  = r'>'

# -----------------------------------------------------------------------------
# 4) Operadores de atribuição composta (lista antes do simples)

t_PLUSEQ   = r'\+='
t_MINUSEQ  = r'-='
t_TIMESEQ  = r'\*='
t_DIVEQ    = r'/='

# 5) Operador de atribuição simples “=”
t_EQUALS   = r'='

# -----------------------------------------------------------------------------
# 6) Operadores aritméticos simples

t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'

# -----------------------------------------------------------------------------
# 7) Literais de caractere e string

t_CHAR_LITERAL   = r"'(\\.|[^\\'])'"
t_STRING_LITERAL = r'"(\\.|[^\\"])*"'

# -----------------------------------------------------------------------------
# 8) Identificador e distinção de palavras-reservadas

def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# -----------------------------------------------------------------------------
# 9) Números inteiros ou reais

def t_NUMBER(t):
    r'\d+(?:\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# -----------------------------------------------------------------------------
# 10) Comentários (ignorados)

def t_COMMENT(t):
    r'//.*'
    pass

def t_COMMENT_BLOCK(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

# -----------------------------------------------------------------------------
# 11) Ignorar espaços, tabs e quebras de linha

t_ignore = ' \t\r\n'

# -----------------------------------------------------------------------------
# 12) Tratamento de erro léxico

def t_error(t):
    print(f"Erro léxico: caractere inválido '{t.value[0]}' (linha {t.lineno})")
    t.lexer.skip(1)

# -----------------------------------------------------------------------------
# 13) Criação do analisador léxico

lexer = lex.lex()

# -----------------------------------------------------------------------------
# 14) Precedência para expressões aritméticas

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# -----------------------------------------------------------------------------
# 15) Início da gramática

start = 'program'

# -----------------------------------------------------------------------------
# 16) Produções sintáticas

# Programa = lista de statements
def p_program(p):
    """
    program : stmt_list
    """
    p[0] = p[1]

# Lista de statements (pode ser vazia)
def p_stmt_list(p):
    """
    stmt_list : stmt stmt_list
              | empty
    """
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

# Cada stmt pode ser declaração, atribuição, if, switch ou break
def p_stmt(p):
    """
    stmt : var_decl
         | assign_stmt
         | if_stmt
         | switch_stmt
         | break_stmt
    """
    p[0] = p[1]

# --------------------------------------------------------------------------
# 1) Declaração de variável
def p_var_decl(p):
    """
    var_decl : TYPE declarator_list SEMICOLON
    """
    p[0] = ('decl', p[1], p[2])

def p_declarator_list_single(p):
    "declarator_list : declarator"
    p[0] = [p[1]]

def p_declarator_list_multi(p):
    "declarator_list : declarator_list COMMA declarator"
    p[0] = p[1] + [p[3]]

def p_declarator_no_init(p):
    "declarator : ID"
    p[0] = ('var', p[1], None)

def p_declarator_init(p):
    "declarator : ID EQUALS initializer"
    p[0] = ('var', p[1], p[3])

def p_initializer_number(p):
    "initializer : NUMBER"
    p[0] = p[1]

def p_initializer_char(p):
    "initializer : CHAR_LITERAL"
    p[0] = p[1]

def p_initializer_string(p):
    "initializer : STRING_LITERAL"
    p[0] = p[1]

# --------------------------------------------------------------------------
# 2) Atribuição aritmética simples
def p_assign_stmt(p):
    """
    assign_stmt : ID assign_op expr SEMICOLON
    """
    p[0] = ('assign', p[1], p[2], p[3])

def p_assign_op(p):
    """
    assign_op : EQUALS
              | PLUSEQ
              | MINUSEQ
              | TIMESEQ
              | DIVEQ
    """
    p[0] = p[1]

# --------------------------------------------------------------------------
# 3) Expressões aritméticas
def p_expr_plus(p):
    "expr : expr PLUS term"
    p[0] = ('+', p[1], p[3])

def p_expr_minus(p):
    "expr : expr MINUS term"
    p[0] = ('-', p[1], p[3])

def p_expr_term(p):
    "expr : term"
    p[0] = p[1]

def p_term_times(p):
    "term : term TIMES factor"
    p[0] = ('*', p[1], p[3])

def p_term_div(p):
    "term : term DIVIDE factor"
    p[0] = ('/', p[1], p[3])

def p_term_factor(p):
    "term : factor"
    p[0] = p[1]

def p_factor_id(p):
    "factor : ID"
    p[0] = ('id', p[1])

def p_factor_num(p):
    "factor : NUMBER"
    p[0] = ('num', p[1])

def p_factor_paren(p):
    "factor : LPAREN expr RPAREN"
    p[0] = p[2]

# --------------------------------------------------------------------------
# 4) Condição relacional (para uso em if)
def p_cond(p):
    "cond : expr relop expr"
    p[0] = ('cond', p[2], p[1], p[3])

def p_relop(p):
    """
    relop : EQ
          | NE
          | LT
          | LE
          | GT
          | GE
    """
    p[0] = p[1]

# --------------------------------------------------------------------------
# 5) Comando IF [ ELSE ]
def p_if_stmt(p):
    """
    if_stmt : IF LPAREN cond RPAREN compound_stmt opt_else
    """
    p[0] = ('if', p[3], p[5], p[6])

def p_opt_else(p):
    """
    opt_else : ELSE compound_stmt
             | empty
    """
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

# --------------------------------------------------------------------------
# 6) Comando SWITCH‐CASE

def p_switch_stmt(p):
    """
    switch_stmt : SWITCH LPAREN ID RPAREN LBRACE case_block_list opt_default RBRACE
    """
    p[0] = ('switch', p[3], p[6], p[7])

def p_case_block_list(p):
    """
    case_block_list : case_block case_block_list
                    | empty
    """
    if len(p) == 3:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = []

def p_case_block(p):
    """
    case_block : case_label_list compound_stmt
    """
    p[0] = ('case', p[1], p[2])

# Lista de rótulos “CASE ID COLON” (um ou mais)
def p_case_label_list_single(p):
    "case_label_list : CASE ID COLON"
    p[0] = [p[2]]

def p_case_label_list_multi(p):
    "case_label_list : CASE ID COLON case_label_list"
    p[0] = [p[2]] + p[4]

# Bloco default
def p_opt_default(p):
    """
    opt_default : DEFAULT COLON compound_stmt
                | empty
    """
    if len(p) == 4:
        p[0] = ('default', p[3])
    else:
        p[0] = None

# --------------------------------------------------------------------------
# 7) Bloco composto (usado em if, switch e outros contextos)
def p_compound_stmt(p):
    "compound_stmt : LBRACE stmt_list RBRACE"
    p[0] = ('block', p[2])

# --------------------------------------------------------------------------
# 8) Comando BREAK
def p_break_stmt(p):
    "break_stmt : BREAK SEMICOLON"
    p[0] = ('break',)

# --------------------------------------------------------------------------
# 9) Produção “empty” para listas opcionais
def p_empty(p):
    "empty :"
    p[0] = []

# --------------------------------------------------------------------------
# 10) Tratamento de erros sintáticos
def p_error(p):
    if p:
        print(f"Erro sintático: token inesperado '{p.value}' (linha {p.lineno})")
    else:
        print("Erro sintático: fim de entrada inesperado")

# -----------------------------------------------------------------------------
# 11) Construção do parser

parser = yacc.yacc()

# -----------------------------------------------------------------------------
# 12) Função para processar uma entrada completa (uma unidade de declaração)

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
# 13) Rotina principal com buffering de linhas para suportar blocos if/switch

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

            buffer += line + "\n"
            brace_balance += line.count('{') - line.count('}')

            if brace_balance == 0:
                stripped = buffer.strip()
                if stripped:
                    process_input(buffer)
                buffer = ""
                brace_balance = 0

    elif len(sys.argv) == 2 and sys.argv[1].endswith('.txt'):
        # Arquivo de declarações em lote: processa todo o conteúdo de uma vez
        arquivo = sys.argv[1]
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                content = f.read()
                process_input(content)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {arquivo}")

    elif len(sys.argv) == 2:
        # Declaração única passada como argumento
        process_input(sys.argv[1])

    else:
        print("Uso:")
        print("  python analisador_c_selecao.py              # modo interativo")
        print("  python analisador_c_selecao.py arquivo.txt  # processa arquivo completo (blocos multilinha)")
        print("  python analisador_c_selecao.py \"if(x<10){y=2;}\"")
        sys.exit(1)

if __name__ == '__main__':
    main()
