import customtkinter as ctk
from Modules.componentsGUI.Menu_Bar import MenuBar
from Modules.componentsGUI.Text_Areas import TextAreas
from Modules.componentsGUI.File_Handler import FileHandler
from Modules.componentsGUI.Status_Bar import StatusBar
from Modules.Lexer_Core import LexerCore

class LexerGUI:
    """
    Graphical User Interface (GUI) for the Base Lexer application.

    This class sets up the main application window and integrates all
    GUI components such as the menu bar, text areas, status bar, and
    connects them to the core lexer engine.

    Attributes
    ----------
    root : ctk.CTk
        The main application window.
    file_handler : FileHandler
        Component responsible for file operations.
    menu_bar : MenuBar
        The top menu bar of the application.
    text_areas : TextAreas
        Component managing input and output text areas.
    status_bar : StatusBar
        The bottom status bar displaying messages.
    lexer : LexerCore
        The core lexer engine responsible for lexical and syntactic analysis.
    """
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title("Base Lexer BY @Ch4rum")
        self.root.geometry("720x820")
        self.file_handler = FileHandler()
        self.menu_bar = MenuBar(self.root, self.file_handler)
        self.text_areas = TextAreas(self.root)
        self.status_bar = StatusBar(self.root)
        self.lexer = LexerCore()
        self.menu_bar.set_run_callback(self.run_button_callback)
        self.setup_ui()

    def setup_ui(self) -> None:
        """
        Configures and initializes all user interface components.

        Creates the menu bar, text areas, and status bar components,
        then establishes the necessary connections between them for
        proper application functionality.

        Returns
        -------
            None
        """
        self.menu_bar.create_menu_bar()
        self.text_areas.create_areas()
        self.file_handler.set_text_areas(self.text_areas)
        self.status_bar.create_status_bar()
        self.file_handler.set_status_bar(self.status_bar)
        self.menu_bar.set_status_bar(self.status_bar)

    def run_button_callback(self) -> None:
        """
        Callback function for the run button execution.

        Processes the input code through lexical and syntactic analysis,
        clears previous output, and displays the results including tokens,
        AST, and any errors encountered during processing.

        Returns
        -------
        None
            This function does not return any value but updates the GUI
            components with the processing results.
        """
        self.text_areas.clear_output()
        code = self.text_areas.get_text().strip()
        if not code:
            self.status_bar.set_text("No input to process")
            self.text_areas.append_to_output("⚠️ No input provided.")
            return
        self.status_bar.set_text("Running...")
        self.text_areas.append_to_output("Running...")
        try:
            result = self.lexer.process(code)
            self.text_areas.append_to_output("\n--- TOKENS ---")
            for token in result["tokens"]:
                self.text_areas.append_to_output(str(token))
            if result["lexer_errors"]:
                self.text_areas.append_to_output("\n--- LEXER ERRORS ---")
                for err in result["lexer_errors"]:
                    self.text_areas.append_to_output(str(err))
            else:
                self.text_areas.append_to_output("\nNo lexer errors.")
            self.text_areas.append_to_output("\n--- AST ---")
            self.text_areas.append_to_output(str(result["ast"]))
            if result["parser_errors"]:
                self.text_areas.append_to_output("\n--- PARSER ERRORS ---")
                for err in result["parser_errors"]:
                    self.text_areas.append_to_output(str(err))
            else:
                self.text_areas.append_to_output("\nNo parser errors.")
            self.status_bar.set_text("Execution completed")
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.text_areas.append_to_output(error_msg)
            self.status_bar.show_error(error_msg)


    def exit(self) -> None:
        """
        Terminates the application execution.

        Forces the application to close by invoking the menu bar's
        exit functionality.

        Parameters
        ----------
        forced : bool, optional
            Indicates whether to force the application exit without
            prompting for confirmation. Default is True.

        Returns
        -------
            None
        """
        self.menu_bar.exit_app(forced=True)

    def run(self) -> None:
        """
        Initializes and starts the main application event loop.

        This method begins the GUI processing and handles all user
        interactions until the application is terminated.

        Returns
        -------
            None
        """
        self.root.mainloop()
