
class PositionCalculator:
    """
    Provides static methods for calculating text positions and context.

    This utility class handles position calculations for error reporting
    and context display in the lexer and parser.
    """
    @staticmethod
    def calculate_column(lexer_data: str, lexpos: int) -> int:
        """
        Calculates the column number for a given position in the text.

        Parameters
        ----------
        lexer_data : str
            The complete input text being analyzed.
        lexpos : int
            The absolute position in the text.

        Returns
        -------
        int
            The column number (1-based) at the given position.
        """
        last_nl = lexer_data.rfind('\n', 0, lexpos)
        if last_nl < 0:
            return lexpos + 1
        return (lexpos - last_nl)

    @staticmethod
    def get_position_context(lexer_data: str, lexpos: int, context_lines: int = 2) -> str:
        """
        Generates contextual text around a specific position for error reporting.

        Parameters
        ----------
        lexer_data : str
            The complete input text being analyzed.
        lexpos : int
            The absolute position in the text.
        context_lines : int, optional
            Number of lines to include before and after the error line, by default 2.

        Returns
        -------
        str
            A formatted string showing the context around the position with line numbers
            and a pointer to the specific column.
        """
        lines = lexer_data.split('\n')
        line_num = lexer_data.count('\n', 0, lexpos)
        start_line = max(0, line_num - context_lines)
        end_line = min(len(lines), line_num + context_lines + 1)
        context = []
        for i in range(start_line, end_line):
            prefix = ">>> " if i == line_num else "    "
            context.append(f"{prefix}{i+1}: {lines[i]}")
            if i == line_num:
                col = PositionCalculator.calculate_column(lexer_data, lexpos)
                context.append(" " * (col+6) + "^")
        return '\n'.join(context)
