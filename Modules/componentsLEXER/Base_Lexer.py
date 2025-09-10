import ply.lex as lex
from Modules.componentsLEXER.Position import PositionCalculator
from Modules.componentsLEXER.Core_Errors import LexerError
from Modules.componentsLEXER.Core_Tokens import ALL_TOKENS, RESERVED, SYMBOLS, IGNORE
from Modules.componentsLEXER.Core_States import LEXER_STATES

class BaseLexer:
    """
    Base lexical analyzer (lexer) for the programming language.

    This class handles tokenization of source code using PLY lex,
    including error handling, position tracking, and support for
    various language features like comments and strings.

    Attributes
    ----------
    states : tuple
        Lexer states for handling different contexts.
    tokens : list
        List of all token types recognized by the lexer.
    reserved : dict
        Dictionary of reserved keywords and their token types.
    t_ignore : str
        Characters to ignore during tokenization in initial state.
    t_str_ignore : str
        Characters to ignore in string state.
    t_raw_ignore : str
        Characters to ignore in raw string state.
    t_comment_ignore : str
        Characters to ignore in comment state.
    """
    states = LEXER_STATES
    tokens = ALL_TOKENS
    reserved = RESERVED
    t_ignore = IGNORE
    t_str_ignore = ''
    t_raw_ignore = ''
    t_comment_ignore = ''

    def __init__(self):
        self.errors = []
        self.lexer = lex.lex(module=self)
        self._position_calc = PositionCalculator()

    def tokenize(self, text: str) -> list:
        """
        Tokenizes the input text and returns a list of tokens.

        Parameters
        ----------
        text : str
            The source code to be tokenized.

        Returns
        -------
        list
            List of tokens generated from the input text.
        """
        self.errors.clear()
        self.lexer.input(text)
        tokens = []
        while True:
            tokk = self.lexer.token()
            if not tokk:
                break
            tokens.append(tokk)
        return tokens
    
    def get_errors(self) -> list:
        """
        Returns a copy of the current lexer errors.

        Returns
        -------
        list
            List of LexerError objects encountered during tokenization.
        """
        return self.errors.copy()

    def add_lexer_error(self, lineno: int, lexpos: int, message: str) -> None:
        """
        Adds a lexer error with position information and context.

        Parameters
        ----------
        lineno : int
            Line number where the error occurred.
        lexpos : int
            Lexical position where the error occurred.
        message : str
            Error message description.

        Returns
        -------
            None
        """
        col = self._position_calc.calculate_column(self.lexer.lexdata, lexpos)
        context = self._position_calc.get_position_context(self.lexer.lexdata, lexpos)
        self.errors.append(LexerError(lineno, col, message, context))

    def t_IDENT(self, t):
        r'[A-Za-z_][A-Za-z0-9_]*'
        t.type = self.reserved.get(t.value, 'IDENT')
        return t

    def t_NUMBER(self, t):
        r'(?:0|[1-9][0-9]*)'
        t.value = int(t.value)
        return t

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_COMMENT(self, t):
        r'\#.*'
        pass

    def t_LINE_COMMENT(self, t):
        r'//.*'
        pass

    def t_COMMENT_START(self, t):
        r'/\*'
        t.lexer.comment_level = 1
        t.lexer.begin('comment')

    def t_comment_COMMENT_START(self, t):
        r'/\*'
        t.lexer.comment_level += 1

    def t_comment_COMMENT_END(self, t):
        r'\*/'
        t.lexer.comment_level -= 1
        if t.lexer.comment_level == 0:
            t.lexer.begin('INITIAL')

    def t_comment_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    def t_comment_anything(self, t):
        r'[^\*/]+'
        pass

    def t_comment_error(self, t):
        self.add_lexer_error(t.lineno, t.lexpos, "Illegal character in comment")
        t.lexer.skip(1)

    def t_comment_eof(self, t):
        self.add_lexer_error(
            t.lexer.lineno,
            len(t.lexer.lexdata),
            "EOF reached before closing multiline comment"
        )
        return None

    def t_STRING(self, t):
        r'["\']'
        t.lexer.string = ''
        t.lexer.quote = t.value
        t.lexer.begin('str')

    def t_str_end(self, t):
        r'["\']'
        if t.value == t.lexer.quote:
            t.value = t.lexer.string
            t.type = 'STRING'
            t.lexer.begin('INITIAL')
            return t
        else:
            t.lexer.string += t.value

    def t_str_escaped_quote(self, t):
        r'\\"|\\\''
        quote = t.value[1]
        t.lexer.string += quote

    def t_str_newline(self, t):
        r'\n'
        self.add_lexer_error(t.lineno, t.lexpos, "Unclosed string literal")
        t.lexer.skip(1)
        t.lexer.begin('INITIAL')

    def t_str_content(self, t):
        r'[^"\n\\\']+'
        t.lexer.string += t.value

    def t_str_error(self, t):
        self.add_lexer_error(t.lineno, t.lexpos, f"Illegal character in string: {t.value[0]!r}")
        t.lexer.skip(1)

    def t_RAW_STRING(self, t):
        r'`'
        t.lexer.raw = ''
        t.lexer.begin('raw')

    def t_raw_end(self, t):
        r'`'
        t.value = t.lexer.raw
        t.type = 'RAW_STRING'
        t.lexer.begin('INITIAL')
        return t

    def t_raw_content(self, t):
        r'[^`]+'
        t.lexer.raw += t.value

    def t_raw_eof(self, t):
        self.add_lexer_error(t.lexer.lineno, t.lexpos, "EOF in raw string")
        return None

    def t_raw_error(self, t):
        self.add_lexer_error(t.lineno, t.lexpos, f"Illegal character in raw string: {t.value[0]!r}")
        t.lexer.skip(1)

    def t_error(self, t):
        self.add_lexer_error(t.lineno, t.lexpos, f"Illegal character: {t.value[0]!r}")
        t.lexer.skip(1)

for symbol_name, pattern in SYMBOLS.items():
    setattr(BaseLexer, f"t_{symbol_name}", pattern)
