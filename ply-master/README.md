# Analisador de Declarações em C

Este repositório contém um analisador léxico e sintático em Python, usando PLY (Python Lex-Yacc), para reconhecimento de declarações de variáveis no estilo da linguagem C.

## Requisitos

- Python 3.x
- PLY

## Instalação

```bash
pip install ply
```

## Uso

### Modo Interativo

1. Abra o terminal na pasta do projeto.
2. Execute:
   ```bash
   python analisador_c_.py
   ```
3. No prompt, digite sua declaração (ex.: `int x;`, `float y = 3.14;`, `char s = "oi";`) e pressione Enter.
4. Para sair, digite `exit`.

### Linha de Comando

Você também pode processar um arquivo de declarações em lote:

```bash
python analisador_c_.py entradas.txt
```

Ou passar uma única declaração como argumento:

```bash
python analisador_c_.py "int x = 42;"
```

O analisador exibirá:

1. **Tokens reconhecidos** pela análise léxica;
2. **Resultado da análise sintática** (declaração válida ou mensagem de erro).

## Exemplos

```bash
$ python analisador_c_.py
Analisador pronto. Digite 'exit' para sair.
> float z = (3.14 * r) / -2e3;

Tokens reconhecidos:
  TYPE            'float'
  ID              'z'
  EQUALS          '='
  LPAREN          '('
  NUMBER          3.14
  TIMES           '*'
  ID              'r'
  RPAREN          ')'
  DIVIDE          '/'
  MINUS           '-'
  NUMBER          2000.0
  SEMICOLON       ';'

Declaração válida: ('decl', 'float', [('var', 'z', ('binop', '/', ('binop', '*', 3.14, 'r'), ('uminus', 2000.0)))] )
> exit
```

```bash
$ python analisador_c_.py "int a, b = 2, c;"

Tokens reconhecidos:
  TYPE            'int'
  ID              'a'
  COMMA           ','
  ID              'b'
  EQUALS          '='
  NUMBER          2
  COMMA           ','
  ID              'c'
  SEMICOLON       ';'

Declaração válida: ('decl', 'int', [('var','a',None),('var','b',2),('var','c',None)])
```

## Tokens Reconhecidos

- **TYPE**: `int`, `float`, `char`
- **ID**: identificadores válidos (`[A-Za-z_][A-Za-z0-9_]*`)
- **NUMBER**: inteiros e floats (`123`, `3.14`)
- **CHAR_LITERAL**: literais de caractere (`'x'`, `"
"`)
- **STRING_LITERAL**: cadeias de caracteres (`"texto"`)
- **EQUALS**: `=` 
- **COMMA**: `,`
- **SEMICOLON**: `;`

## Licença

MIT
