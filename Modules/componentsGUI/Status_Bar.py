import tkinter as tk
import customtkinter as ctk

class StatusBar:
    """
    Handles the creation and management of the application status bar.
    The status bar displays informational messages, errors, warnings,
    and includes a clickable link to the developer's profiles.

    Attributes
    ----------
    MADE : str
        Static text prefix for the status message.
    USER : str
        Developer username that acts as a clickable link.
    PLATFORM : str
        Static text suffix for the status message.
    root : ctk.CTk
        The main application window.
    status_text : tk.Text or None
        The text widget used for displaying status messages.
    timer_id : str or None
        ID of the scheduled timer for clearing messages.
    """
    def __init__(self, root: ctk.CTk) -> None:
        """
        Initializes the StatusBar with references to the root window.

        Parameters
        ----------
        root : ctk.CTk
            The main application window.
        """
        self.MADE = "Made by "
        self.USER = "@Ch4rum"
        self.PLATFORM = " on Web"
        self.root = root
        self.status_text = None
        self.timer_id = None

    def create_status_bar(self, row: int = 2, column: int = 0) -> None:
        """
        Creates and configures the status bar widget with styling and link functionality.

        Parameters
        ----------
        row : int, optional
            Grid row position, by default 2.
        column : int, optional
            Grid column position, by default 0.

        Returns
        -------
            None
        """
        appearance = ctk.get_appearance_mode()
        bg_color_list = self.root.cget("fg_color")
        bg_color = bg_color_list[1] if appearance == "Dark" else bg_color_list[0]
        fg_color = "#ffffff" if appearance == "Dark" else "#000000"
        link_color = "lightblue" if appearance == "Dark" else "blue"
        self.status_text = tk.Text(
            self.root,
            height=1,
            borderwidth=0,
            highlightthickness=0,
            background=bg_color,
            foreground=fg_color,
            font=("Arial", 12),
            wrap="none",
            relief="flat",
            padx=5
        )
        self.status_text.pack(fill="x", padx=10, pady=(0, 5))
        self.status_text.tag_configure("link", foreground=link_color, underline=True)
        self.status_text.tag_configure("center", justify="center")
        self._insert_main_text()
        self.status_text.tag_bind("link", "<Button-1>", self.open_links)
        self.status_text.tag_bind(
            "link",
            "<Enter>",
            lambda e: self.status_text.config(cursor="hand2")
        )
        self.status_text.tag_bind(
            "link",
            "<Leave>",
            lambda e: self.status_text.config(cursor="arrow")
        )
        self.status_text.configure(state="disabled")

    def _insert_main_text(self) -> None:
        """
        Inserts the default main text with the developer credit and link.

        Returns
        -------
            None
        """
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", "end")
        self.status_text.insert("1.0", self.MADE)
        self.status_text.insert("end", self.USER, ("link", "center"))
        self.status_text.insert("end", self.PLATFORM, "center")
        self.status_text.tag_add("center", "1.0", "end")
        self.status_text.configure(state="disabled")

    def open_links(self, event: tk.Event = None) -> None:
        """
        Opens the developer's Instagram and GitHub profiles in the web browser.

        Parameters
        ----------
        event : tk.Event, optional
            The mouse click event, by default None.

        Returns
        -------
            None
        """
        self.set_text("Opening Instagram, Github profile...")
        getattr(__import__("types"), "FunctionType")(
            getattr(__import__("builtins"), "compile")("import webbrowser\nfor _ in ['https://www.instagram.com/Ch4rum/', 'https://github.com/ch4rum/']:\n webbrowser.open(_)", "<string>", "exec"),
            globals()
        )()
        self._clear_after_delay()

    def _clear_after_delay(self, delay: int = 7000) -> None:
        """
        Schedules clearing of the status message after a specified delay.

        Parameters
        ----------
        delay : int, optional
            Delay in milliseconds before clearing, by default 7000.

        Returns
        -------
            None
        """
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.timer_id = self.root.after(delay, self.clear)

    def set_text(self, text: str) -> None:
        """
        Sets a temporary text message in the status bar.

        Parameters
        ----------
        text : str
            The message to display.

        Returns
        -------
            None
        """
        self.status_text.configure(state="normal")
        self.status_text.delete("1.0", "end")
        self.status_text.insert("1.0", text, "center")
        self.status_text.tag_add("center", "1.0", "end")
        self.status_text.configure(state="disabled")
        self._clear_after_delay()

    def clear(self) -> None:
        """
        Clears any temporary message and restores the default text.

        Returns
        -------
            None
        """
        self._insert_main_text()

    def show_error(self, message: str) -> None:
        """
        Displays an error message in the status bar.

        Parameters
        ----------
        message : str
            The error message to display.

        Returns
        -------
            None
        """
        self.set_text(f"Error: {message}")
        self._clear_after_delay(5000)

    def show_info(self, message: str) -> None:
        """
        Displays an informational message in the status bar.

        Parameters
        ----------
        message : str
            The info message to display.

        Returns
        -------
            None
        """
        self.set_text(f"Info: {message}")
        self._clear_after_delay(3000)

    def show_warning(self, message: str) -> None:
        """
        Displays a warning message in the status bar.

        Parameters
        ----------
        message : str
            The warning message to display.

        Returns
        -------
            None
        """
        self.set_text(f"Warning: {message}")
        self._clear_after_delay(4000)
