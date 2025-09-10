from tkinter import messagebox
import customtkinter as ctk

class MenuBar:
    """
    Handles the creation and functionality of the application menu bar.

    Attributes
    ----------
    root : ctk.CTk
        The main application window.
    file_handler : FileHandler
        Component responsible for file operations.
    run_callback : callable or None
        Callback function for the run button action.
    status_bar : StatusBar or None
        Reference to the status bar component.
    """
    def __init__(self, root: ctk.CTk, file_handler: 'FileHandler') -> None:
        """
        Initializes the MenuBar with references to root window and file handler.

        Parameters
        ----------
        root : ctk.CTk
            The main application window.
        file_handler : FileHandler
            Component responsible for file operations.
        """
        self.root = root
        self.file_handler = file_handler
        self.menu_frame = None
        self.file_menu = None
        self.run_button = None
        self.run_callback = None
        self.status_bar = None

    def set_run_callback(self, callback: 'Callable') -> None:
        """
        Sets the callback function for the run button.

        Parameters
        ----------
        callback : Callable
            Function to be called when the run button is pressed.

        Returns
        -------
            None
        """
        self.run_callback = callback

    def set_status_bar(self, status_bar: 'StatusBar') -> None:
        """
        Sets the reference to the status bar component.

        Parameters
        ----------
        status_bar : StatusBar
            The status bar component for displaying messages.

        Returns
        -------
            None
        """
        self.status_bar = status_bar

    def create_menu_bar(self) -> None:
        """
        Creates and configures the menu bar with file options and run button.

        Returns
        -------
            None
        """
        self.menu_frame = ctk.CTkFrame(self.root, height=35, fg_color="transparent")
        self.menu_frame.pack(fill="x", padx=10, pady=(10, 0))
        self.file_menu = ctk.CTkOptionMenu(
            self.menu_frame,
            values=["New", "Open", "Save", "Exit"],
            command=self.file_menu_callback,
            width=110,
            height=30,
            font=("Arial", 15),
            dropdown_font=("Arial", 14)
        )
        self.file_menu.set("File")
        self.file_menu.pack(side="left", padx=10, pady=2)
        self.customize_dropdown()
        self.run_button = ctk.CTkButton(
            self.menu_frame,
            text="Run",
            width=100,
            height=30,
            command=self.run_button_callback
        )
        self.run_button.pack(side="left", padx=10, pady=2)

    def customize_dropdown(self) -> None:
        """
        Schedules delayed customization of the dropdown menu appearance.

        Returns
        -------
            None
        """
        self.root.after(100, self._delayed_customize_dropdown)

    def _delayed_customize_dropdown(self) -> None:
        """
        Applies custom styling to the dropdown menu after a short delay.

        Returns
        -------
            None
        """
        try:
            if hasattr(self.file_menu, '_dropdown_menu'):
                self.file_menu._dropdown_menu.configure(
                    fg_color=("#f0f0f0", "#2b2b2b"),
                    text_color=("#0000FF", "#FFA500")
                )
                for widget in self.file_menu._dropdown_menu.winfo_children():
                    if isinstance(widget, ctk.CTkButton):
                        widget.configure(height=40)
        except Exception as e:
            print("Error al personalizar dropdown:", e)

    def file_menu_callback(self, choice: str) -> None:
        """
        Handles file menu option selections.

        Parameters
        ----------
        choice : str
            The selected menu option ("New", "Open", "Save", or "Exit").

        Returns
        -------
            None
        """
        self.file_menu.set("File")
        if choice == "New":
            self.file_handler.new_file()
        elif choice == "Open":
            self.file_handler.open_file()
        elif choice == "Save":
            self.file_handler.save_file()
        elif choice == "Exit":
            self.exit_app()

    def run_button_callback(self) -> None:
        """
        Executes the run callback function when the run button is pressed.

        Returns
        -------
            None
        """
        if self.run_callback:
            self.run_callback()

    def exit_app(self, forced: bool = False) -> None:
        """
        Handles application exit with optional forced closure.

        Parameters
        ----------
        forced : bool, optional
            If True, skips confirmation dialog, by default False.

        Returns
        -------
            None
        """
        if forced or self.file_handler.save_check():
            if forced or messagebox.askokcancel(
                "Exit Application",
                "Are you sure you want to exit?"
            ):
                if self.status_bar:
                    self.status_bar.show_warning("Closing application")
                self.root.quit()
