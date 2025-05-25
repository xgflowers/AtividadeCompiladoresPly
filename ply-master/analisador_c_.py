#!/usr/bin/env python3
import sys
import ply.lex as lex
import ply.yacc as yacc

# ---------- Tokens ----------

tokens = (
    'TYPE', 'ID', 'NUMBER', 'CHAR_LITERAL', 'STRING_LITERAL',
    'EQUALS', 'COMMA', 'SEMICOLON'
)

# Símbolos literais

t_EQUALS    = r'='
t_COMMA     = r','
t_SEMICOLON = r';'

# Palavras reservadas (tipos)
reserved = {
    'int':   'TYPE',
    'float': 'TYPE',
    'char':  'TYPE'
}

# Identificadores: letra ou '_' seguido de letras, dígitos ou '_'
def t_ID(t):
    r'[A-Za-z_][A-Za-z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Números inteiros ou float (sem exponencial)
def t_NUMBER(t):
    r'\d+(?:\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Literais de caractere único
def t_CHAR_LITERAL(t):
    r"'(\\.|[^\\'])'"
    t.value = t.value[1:-1]
    return t

# Literais de cadeia de caracteres
def t_STRING_LITERAL(t):
    r'"(\\.|[^\\"])*"'
    t.value = t.value[1:-1]
    return t

# Comentários de linha (//...)
def t_COMMENT(t):
    r'//.*'
    pass

# Comentários em bloco (/*...*/)
def t_COMMENT_BLOCK(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

# Ignorar espaços, tabs e quebras de linha
t_ignore = ' \t\n'

def t_error(t):
    print(f"Erro léxico: caractere inválido '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# ---------- Gramática ----------

# declaration : TYPE declarator_list SEMICOLON
def p_declaration(p):
    'declaration : TYPE declarator_list SEMICOLON'
    p[0] = ('decl', p[1], p[2])
    print('Declaração válida:', p[0])

# declarator_list : declarator (COMMA declarator)*
def p_declarator_list_single(p):
    'declarator_list : declarator'
    p[0] = [p[1]]

def p_declarator_list_multi(p):
    'declarator_list : declarator_list COMMA declarator'
    p[0] = p[1] + [p[3]]

# declarator : ID | ID EQUALS initializer
def p_declarator_no_init(p):
    'declarator : ID'
    p[0] = ('var', p[1], None)

def p_declarator_init(p):
    'declarator : ID EQUALS initializer'
    p[0] = ('var', p[1], p[3])

# initializer : NUMBER | CHAR_LITERAL | STRING_LITERAL
def p_initializer_number(p):
    'initializer : NUMBER'
    p[0] = p[1]

def p_initializer_char(p):
    'initializer : CHAR_LITERAL'
    p[0] = p[1]

def p_initializer_string(p):
    'initializer : STRING_LITERAL'
    p[0] = p[1]

# Tratamento de erros sintáticos
def p_error(p):
    if p:
        print(f"Erro sintático: token inesperado '{p.value}'")
    else:
        print("Erro sintático: fim de entrada inesperado")

parser = yacc.yacc()

# Processa uma linha de declaração
def process_line(line):
    print("\nTokens reconhecidos:")
    lexer.input(line)
    for tok in lexer:
        print(f"  {tok.type:15} {tok.value!r}")
    parser.parse(line, lexer=lexer)

# Leitura de arquivo .txt, declaração única ou modo interativo
def main():
    # Modo interativo
    if len(sys.argv) == 1:
        print("Analisador pronto. Digite 'exit' para sair.")
        while True:
            try:
                line = input('> ')
            except EOFError:
                break
            if line.lower() == 'exit':
                break
            if line.strip():
                process_line(line)
    # Arquivo de declarações em lote
    elif len(sys.argv) == 2 and sys.argv[1].endswith('.txt'):
        arquivo = sys.argv[1]
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        process_line(line)
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {arquivo}")
    # Declaração única como argumento
    elif len(sys.argv) == 2:
        process_line(sys.argv[1])
    else:
        print("Uso:")
        print("  python analisador_c_.py            # modo interativo")
        print("  python analisador_c_.py arquivo.txt  # processa lote de declarações")
        print("  python analisador_c_.py \"int x = 42;\"    # declaração única")
        sys.exit(1)

if __name__ == '__main__':
    main()
