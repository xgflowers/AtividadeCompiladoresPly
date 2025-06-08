# Analisador de Declarações em C

Este repositório contém um analisador léxico e sintático em Python, usando PLY (Python Lex-Yacc), para reconhecimento de:

- Declarações de variáveis no estilo da linguagem C.
- Atribuições aritméticas simples e compostas.
- Reconhecimento de variaveis int, float e char.
- Comandos de seleção (`if` / `else` e `switch` / `case` / `default`).
- Comandos de repetição (while e for).
- Blocos de comandos delimitados por chaves, incluindo suporte a `break;`.

---

## Requisitos

- Python 3.x  
- PLY  

---

## Instalação

```bash
pip install ply

## Uso

### Modo Interativo

1. Abra o terminal na pasta do projeto.
2. Execute:
   ```bash
   python analisador_c_.py
3. No prompt, digite sua instrução C completa (declaração, atribuição, if / else ou switch / case / default) e pressione Enter.

Para blocos multilinha (por exemplo, if (...) { ... } ou switch (...) { ... }), basta digitar as linhas sequencialmente; o analisador só chamará o parser quando todas as chaves { } estiverem fechadas.
Exemplos de prompt:
 	```bash
   	python analisador_c_.py
	Analisador pronto. Digite 'exit' para sair.
	> int x, y = 5;
ou
 	```bash
   	python analisador_c_.py
	> if (x < y) {
	...     z = x + y;
	...     y = y - 1;
	... }
4.Após cada instrução concluída, o analisador exibirá:
	1.Tokens reconhecidos pela análise léxica.
	2.Árvore sintática (AST) gerada pela análise sintática, ou mensagem de erro se a entrada for inválida.
5.Para sair, digite exit.

### Linha de Comando
Você também pode processar um arquivo de declarações em lote:

```bash
python analisador_c_.py entradas.txt
```

## Exemplos

```bash
$ python analisador_c_.py
Analisador pronto. Digite 'exit' para sair.
> int a, b = 2, c;

Tokens reconhecidos:
  TYPE       'int'
  ID         'a'
  COMMA      ','
  ID         'b'
  EQUALS     '='
  NUMBER     2
  COMMA      ','
  ID         'c'
  SEMICOLON  ';'

Árvore sintática (AST):
  [('decl', 'int', [('var','a',None),('var','b',2),('var','c',None)])]
> exit

$ python analisador_c_.py
Analisador pronto. Digite 'exit' para sair.
> x = y + 3 * (z - 1);

Tokens reconhecidos:
  ID         'x'
  EQUALS     '='
  ID         'y'
  PLUS       '+'
  NUMBER     3
  TIMES      '*'
  LPAREN     '('
  ID         'z'
  MINUS      '-'
  NUMBER     1
  RPAREN     ')'
  SEMICOLON  ';'

Árvore sintática (AST):
  [('assign', 'x', '=', ('+', ('id','y'), ('*', ('num',3), ('-', ('id','z'), ('num',1)) )))]
> exit

$ python analisador_c_.py
Analisador pronto. Digite 'exit' para sair.
> if (total >= 100) {
...     desconto = total * 10 / 100;
... }

Tokens reconhecidos:
  IF         'if'
  LPAREN     '('
  ID         'total'
  GE         '>='
  NUMBER     100
  RPAREN     ')'
  LBRACE     '{'
  ID         'desconto'
  EQUALS     '='
  ID         'total'
  TIMES      '*'
  NUMBER     10
  DIVIDE     '/'
  NUMBER     100
  SEMICOLON  ';'
  RBRACE     '}'

Árvore sintática (AST):
  ('if',
    ('cond','>=',('id','total'),('num',100)),
    ('block',[('assign','desconto','=',('/', ('*',('id','total'),('num',10)),('num',100)))]),
    None
  )
> exit

$ python analisador_c_.py
Analisador pronto. Digite 'exit' para sair.
> if (a != b) {
...     c = a + b;
... } else {
...     c = 0;
... }

Tokens reconhecidos:
  IF         'if'
  LPAREN     '('
  ID         'a'
  NE         '!='
  ID         'b'
  RPAREN     ')'
  LBRACE     '{'
  ID         'c'
  EQUALS     '='
  ID         'a'
  PLUS       '+'
  ID         'b'
  SEMICOLON  ';'
  RBRACE     '}'
  ELSE       'else'
  LBRACE     '{'
  ID         'c'
  EQUALS     '='
  NUMBER     0
  SEMICOLON  ';'
  RBRACE     '}'

Árvore sintática (AST):
  ('if',
    ('cond','!=',('id','a'),('id','b')),
    ('block',[('assign','c','+',('id','a','id','b'))]),
    ('block',[('assign','c','=',('num',0))])
  )
> exit

$ python analisador_c_.py
Analisador pronto. Digite 'exit' para sair.
> switch (opcao) {
...     case A: {
...         resposta = 1;
...         break;
...     }
...     case B: {
...         resposta = 2;
...         break;
...     }
...     default: {
...         resposta = 0;
...     }
... }

Tokens reconhecidos:
  SWITCH     'switch'
  LPAREN     '('
  ID         'opcao'
  RPAREN     ')'
  LBRACE     '{'
  CASE       'case'
  ID         'A'
  COLON      ':'
  LBRACE     '{'
  ID         'resposta'
  EQUALS     '='
  NUMBER     1
  SEMICOLON  ';'
  BREAK      'break'
  SEMICOLON  ';'
  RBRACE     '}'
  CASE       'case'
  ID         'B'
  COLON      ':'
  LBRACE     '{'
  ID         'resposta'
  EQUALS     '='
  NUMBER     2
  SEMICOLON  ';'
  BREAK      'break'
  SEMICOLON  ';'
  RBRACE     '}'
  DEFAULT    'default'
  COLON      ':'
  LBRACE     '{'
  ID         'resposta'
  EQUALS     '='
  NUMBER     0
  SEMICOLON  ';'
  RBRACE     '}'
  RBRACE     '}'

Árvore sintática (AST):
  ('switch','opcao', [
      ('case',['A'],('block',[('assign','resposta','=',('num',1)),('break',)])),
      ('case',['B'],('block',[('assign','resposta','=',('num',2)),('break',)]))
    ],
    ('default',('block',[('assign','resposta','=',('num',0))]))
  )
> exit

$ python analisador_c_.py
Analisador pronto. Digite 'exit' para sair.
> switch (codigo) {
...     case X: case Y: case Z: {
...         contador += 1;
...         break;
...     }
...     case W: {
...         contador -= 1;
...         break;
...     }
... }

Tokens reconhecidos:
  SWITCH     'switch'
  LPAREN     '('
  ID         'codigo'
  RPAREN     ')'
  LBRACE     '{'
  CASE       'case'
  ID         'X'
  COLON      ':'
  CASE       'case'
  ID         'Y'
  COLON      ':'
  CASE       'case'
  ID         'Z'
  COLON      ':'
  LBRACE     '{'
  ID         'contador'
  PLUSEQ     '+='
  NUMBER     1
  SEMICOLON  ';'
  BREAK      'break'
  SEMICOLON  ';'
  RBRACE     '}'
  CASE       'case'
  ID         'W'
  COLON      ':'
  LBRACE     '{'
  ID         'contador'
  MINUSEQ    '-='
  NUMBER     1
  SEMICOLON  ';'
  BREAK      'break'
  SEMICOLON  ';'
  RBRACE     '}'
  RBRACE     '}'

Árvore sintática (AST):
  ('switch','codigo', [
      ('case',['X','Y','Z'],('block',[('assign','contador','+=',('num',1)),('break',)])),
      ('case',['W'],       ('block',[('assign','contador','-=',('num',1)),('break',)]))
    ],
    None
  )
> exit

$ python analisador_c_.py
Analisador pronto. Digite 'exit' para sair.
> while (count != 0) {
    count -= 1;
    total = total + count;
}

Tokens reconhecidos:
  WHILE        'while'
  LPAREN       '('
  ID           'count'
  NE           '!='
  NUMBER       0
  RPAREN       ')'
  LBRACE       '{'
  ID           'count'
  MINUSEQ      '-='
  NUMBER       1
  SEMICOLON    ';'
  ID           'total'
  EQUALS       '='
  ID           'total'
  PLUS         '+'
  ID           'count'
  SEMICOLON    ';'
  RBRACE       '}'
Árvore sintática (AST): [('while', ('cond', '!=', ('id', 'count'), ('num', 0)), ('block', [('assign', 'count', '-=', ('num', 1)), ('assign', 'total', '=', ('+', ('id', 'total'), ('id', 'count')))]))]
> exit

$ python analisador_c_.py
Analisador pronto. Digite 'exit' para sair.

for (i = 0; i < n; i += 1) {
    for (j = 0; j < m; j += 1) {
        result = result + 1;
    }
}

Tokens reconhecidos:
  FOR          'for'
  LPAREN       '('
  ID           'i'
  EQUALS       '='
  NUMBER       0
  SEMICOLON    ';'
  ID           'i'
  LT           '<'
  ID           'n'
  SEMICOLON    ';'
  ID           'i'
  PLUSEQ       '+='
  NUMBER       1
  RPAREN       ')'
  LBRACE       '{'
  FOR          'for'
  LPAREN       '('
  ID           'j'
  EQUALS       '='
  NUMBER       0
  SEMICOLON    ';'
  ID           'j'
  LT           '<'
  ID           'm'
  SEMICOLON    ';'
  ID           'j'
  PLUSEQ       '+='
  NUMBER       1
  RPAREN       ')'
  LBRACE       '{'
  ID           'result'
  EQUALS       '='
  ID           'result'
  PLUS         '+'
  NUMBER       1
  SEMICOLON    ';'
  RBRACE       '}'
  RBRACE       '}'
Árvore sintática (AST): [('for', ('init', 'i', '=', ('num', 0)), ('cond', '<', ('id', 'i'), ('id', 'n')), ('iter', 'i', '+=', ('num', 1)), ('block', [('for', ('init', 'j', '=', ('num', 0)), ('cond', '<', ('id', 'j'), ('id', 'm')), ('iter', 'j', '+=', ('num', 1)), ('block', [('assign', 'result', '=', ('+', ('id', 'result'), ('num', 1)))]))]))]
> exit

## Tokens Reconhecidos
TIPOS (TYPE): int, float, char

COMANDOS DE SELEÇÃO:
IF (if)
ELSE (else)
SWITCH (switch)
CASE (case)
DEFAULT (default)
BREAK (break)

COMANDOS DE REPETIÇÃO: 
WHILE (while)
FOR (for)

LITERIAS E IDENTIFICADORES:
ID: identificadores válidos ([A-Za-z_][A-Za-z0-9_]*)
NUMBER: inteiros e floats (123, 3.14, -2.0)
CHAR_LITERAL: literais de caractere (ex.: 'a', '\n')
STRING_LITERAL: cadeias de caracteres (ex.: "texto")

OPERADORES RELACIONAIS:
EQ (==)
NE (!=)
LT (<)
LE (<=)
GT (>)
GE (>=)

OPERADORES ARITMÉTICOS:
PLUS (+)
MINUS (-)
TIMES (*)
DIVIDE (/)

OPERADORES DE ATRIBUIÇÃO:
EQUALS (=)
PLUSEQ (+=)
MINUSEQ (-=)
TIMESEQ (*=)
DIVEQ (/=)

PONTUAÇÃO:
LPAREN (()
RPAREN ())
LBRACE ({)
RBRACE (})
COLON (:)
COMMA (,)
SEMICOLON (;)

## Licença

MIT