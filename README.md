Analisador de Atribuições em C

Este repositório contém um analisador léxico e sintático, em Python, para validar linhas de atribuição simples na linguagem C, usando PLY (Python Lex-Yacc).

Requisitos

Python 3.x

PLY

Instalação do PLY:

pip install ply

Uso

Modo interativo

Abra o terminal na pasta do projeto.

Execute:

python analisador_c_.py

No prompt, digite sua linha de atribuição (ex.: int x = 10 + y;) e pressione Enter.

Para sair, digite exit.

Linha de comando

Você também pode passar a atribuição diretamente como argumento:

python analisador_c_.py "int x = -2.5e1 + y;"

O analisador exibirá:

Tokens reconhecidos pela análise léxica.

Resultado da análise sintática: árvore sintática ou mensagens de erro.

Exemplos

$ python analisador_c_.py
Analisador pronto. Digite 'exit' para sair.
> float z = (3.14 * r) / -2e3;

Tokens reconhecidos:
  TYPE       'float'
  ID         'z'
  EQUALS     '='
  LPAREN     '('
  NUMBER     3.14
  TIMES      '*'
  ID         'r'
  RPAREN     ')'
  DIVIDE     '/'
  MINUS      '-'
  NUMBER     2000.0
  SEMICOLON  ';'

Entrada válida. Árvore sintática: ('assign', 'float', 'z', ('binop', '/', ('binop', '*', 3.14, 'r'), ('uminus', 2000.0)))
> exit

Estrutura de tokens

enumeração dos principais tokens reconhecidos:

TYPE: int, float, char

ID: identificadores válidos ([a-zA-Z_][a-zA-Z0-9_]*)

NUMBER: inteiros, floats e notação exponencial (123, 3.14, 1e-3)

CHAR: literais de caractere ('x', '\n', ''')

PLUS, MINUS, TIMES, DIVIDE, EQUALS, SEMICOLON, LPAREN, RPAREN

Licença

MIT





