
LEXER_STATES = (
    ('str', 'exclusive'),
    ('raw', 'exclusive'),
    ('comment', 'exclusive')
)

PARSER_PRECEDENCE = (
    ('right', 'ASSIGN', 'ASSIGN_VAR'),
    ('left', 'AND'),
    ('left', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULT', 'DIV'),
    ('right', 'NOT')
)