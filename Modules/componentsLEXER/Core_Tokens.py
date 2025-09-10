
TOKENS = (
    'IDENT',       # ID
    'NUMBER',      # Integer
    'PLUS', 'MINUS', 'MULT', 'DIV',  # Arithmetic operators
    'ASSIGN',      # =
    'ASSIGN_VAR',  # :=
    'SEMI',        # ;
    'GT',          # >
    'LT',          # < 
    'GTE',         # >=
    'LTE',         # <=
    'EQ',          # ==
    'NEQ',         # !=
    'LPAREN', 'RPAREN',
    'LBRACE', 'RBRACE',
    'LBRACK', 'RBRACK',
    'STRING',
    'RAW_STRING',
    'AND',         # &&
    'NOT',         # !
    'COLON',       # :
    'COMMA',
    'DOT'
)

RESERVED = {
    'package': 'PACKAGE',
    'import': 'IMPORT',
    'func': 'FUNC',
    'var': 'VAR',
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'return': 'RETURN',
    'int': 'INT',
    'bool': 'BOOL',
    'print': 'PRINT',
    'true': 'TRUE',
    'false': 'FALSE',
}

ALL_TOKENS = TOKENS + tuple(RESERVED.values())

SYMBOLS = {
    'GTE': r'>=',
    'LTE': r'<=',
    'EQ' : r'==',
    'NEQ': r'!=',
    'ASSIGN_VAR': r':=',
    'AND': r'&&',
    'PLUS': r'\+',
    'MINUS': r'-',
    'MULT': r'\*',
    'DIV': r'/',
    'ASSIGN': r'=',
    'SEMI': r';',
    'GT': r'>',
    'LT': r'<',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'LBRACE': r'\{',
    'RBRACE': r'\}',
    'LBRACK': r'\[',
    'RBRACK': r'\]',
    'NOT': r'!',
    'COLON': r':',
    'COMMA': r',',
    'DOT': r'\.'
}

IGNORE = ' \t'

