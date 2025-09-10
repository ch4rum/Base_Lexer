
class LexerError:
    """
    Represents an error encountered during lexical analysis.

    Attributes
    ----------
    lineno : int
        Line number where the error occurred.
    col : int
        Column number where the error occurred.
    message : str
        Description of the error.
    context : str or None, optional
        Additional context information about the error, by default None.
    """
    def __init__(self, lineno: int, col: int, message: str, context: str = None) -> None:
        """
        Initializes a LexerError with position and error information.

        Parameters
        ----------
        lineno : int
            Line number where the error occurred.
        col : int
            Column number where the error occurred.
        message : str
            Description of the error.
        context : str or None, optional
            Additional context information, by default None.
        """
        self.lineno = lineno
        self.col = col
        self.message = message
        self.context = context
    
    def __str__(self) -> str:
        """
        Returns a formatted string representation of the lexer error.

        Returns
        -------
        str
            Formatted error message with line, column, and context.
        """
        if self.context:
            return f"Linea {self.lineno}, Col {self.col}: {self.message}\n{self.context}"
        return f"Linea {self.lineno}, Col {self.col}: {self.message}"

class ParseError:
    """
    Represents an error encountered during syntactic analysis (parsing).

    Attributes
    ----------
    lineno : int
        Line number where the error occurred.
    col : int
        Column number where the error occurred.
    message : str
        Description of the error.
    value : any or None, optional
        The value that caused the error, by default None.
    context : str or None, optional
        Additional context information about the error, by default None.
    """
    def __init__(self, lineno: int, col: int, message: str, value: any = None, context: str = None) -> None:
        """
        Initializes a ParseError with position, error information, and optional value.

        Parameters
        ----------
        lineno : int
            Line number where the error occurred.
        col : int
            Column number where the error occurred.
        message : str
            Description of the error.
        value : any or None, optional
            The value that caused the error, by default None.
        context : str or None, optional
            Additional context information, by default None.
        """
        self.lineno = lineno
        self.col = col
        self.message = message
        self.value =value
        self.context = context

    def __str__(self) -> str:
        """
        Returns a formatted string representation of the parser error.

        Returns
        -------
        str
            Formatted error message with line, column, value, and context.
        """
        base = f"Linea {self.lineno}, Col {self.col}: {self.message}"
        if self.value:
            base += f" at{self.value!r}"
        if self.context:
            base += f"\n{self.context}"
        return base
