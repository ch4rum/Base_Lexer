from typing import Any, Dict

from Modules.componentsLEXER.Language_Parser import LanguageParser

class LexerCore:
    """
    Core class responsible for performing lexical and syntactic analysis
    on a given piece of source code. It utilizes a `LanguageParser` to
    tokenize the input and generate an Abstract Syntax Tree (AST), while
    collecting any errors encountered during the process.

    Attributes
    ----------
    parser : LanguageParser
        Instance of the language parser used for lexical and syntactic analysis.
    """
    def __init__(self):
        self.parser = LanguageParser()

    def process(self, code: str) -> Dict[str, Any]:
        """
        Processes the provided source code by performing both lexical and
        syntactic analysis. Clears previous errors before each stage and
        returns a summary of the results, including the tokens, AST, and
        any errors found.

        Parameters
        ----------
        code : str
            A string representing the source code to be analyzed.

        Returns
        -------
        dict
            A dictionary containing the results of the analysis:
            - 'tokens' : list
                List of tokens generated during lexical analysis.
            - 'ast' : Any
                Abstract Syntax Tree (AST) generated during parsing.
            - 'lexer_errors' : list of str
                List of errors found during lexical analysis.
            - 'parser_errors' : list of str
                List of errors found during syntactic analysis.
        """
        self.parser.errors.clear()
        tokens = self.parser.tokenize(code)
        lexer_errors = self.parser.get_errors()
        self.parser.errors.clear()
        ast = self.parser.parse(code)
        parser_errors = self.parser.get_errors()
        return {
            "tokens": tokens,
            "ast": ast,
            "lexer_errors": lexer_errors,
            "parser_errors": parser_errors
        }
