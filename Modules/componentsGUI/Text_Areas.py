import customtkinter as ctk

class TextAreas:
    """
    Handles the creation and management of text input and output areas.

    This class manages the main text editor area for code input and
    the output area for displaying results, tokens, and errors.

    Attributes
    ----------
    root : ctk.CTk
        The main application window.
    text_area : ctk.CTkTextbox or None
        The text input area for code editing.
    output_area : ctk.CTkTextbox or None
        The text output area for displaying results.
    """
    def __init__(self, root: ctk.CTk) -> None:
        """
        Initializes the TextAreas with reference to the root window.

        Parameters
        ----------
        root : ctk.CTk
            The main application window.
        """
        self.root = root
        self.text_area = None
        self.output_area = None
        self.editor_frame = None

    def create_areas(self) -> None:
        """
        Creates and configures the text input and output areas with proper styling.

        Returns
        -------
            None
        """
        self.editor_frame = ctk.CTkFrame(self.root)
        self.editor_frame.pack(fill="both", expand=True, padx=10, pady=(5, 10))
        self.editor_frame.grid_rowconfigure(0, weight=65)
        self.editor_frame.grid_rowconfigure(1, weight=35)
        self.editor_frame.grid_columnconfigure(0, weight=1)
        self.text_area = ctk.CTkTextbox(
            self.editor_frame,
            wrap="word",
            corner_radius=6,
            border_width=1,
            border_color="#444444"
        )
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=5, pady=(5, 6))
        self.output_area = ctk.CTkTextbox(
            self.editor_frame,
            wrap="word",
            state="disabled",
            corner_radius=6,
            border_width=1,
            border_color="#444444",
            fg_color=("#f0f0f0", "#1a1a1a"),
            text_color=("black", "white")
        )
        self.output_area.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        #self.output_area.bind("<Enter>", lambda e: self._bind_mousewheel(self.output_area))
        #self.output_area.bind("<Leave>", lambda e: self._unbind_mousewheel(self.output_area))

    def get_text(self) -> str:
        """
        Retrieves the current text content from the input area.

        Returns
        -------
        str
            The text content of the input area, stripped of whitespace.
        """
        return self.text_area.get("1.0", ctk.END).strip()

    def set_text(self, text: str) -> None:
        """
        Sets the text content of the input area.

        Parameters
        ----------
        text : str
            The text to be inserted into the input area.

        Returns
        -------
            None
        """
        self.text_area.delete("1.0", ctk.END)
        self.text_area.insert("1.0", text)

    def append_to_output(self, text: str) -> None:
        """
        Appends text to the output area and scrolls to the end.

        Parameters
        ----------
        text : str
            The text to be appended to the output area.

        Returns
        -------
            None
        """
        self.output_area.configure(state="normal")
        self.output_area.insert("end", text + "\n")
        self.output_area.configure(state="disabled")
        self.output_area.see("end")

    def clear_output(self) -> None:
        """
        Clears all content from the output area.

        Returns
        -------
            None
        """
        if self.output_area:
            self.output_area.configure(state="normal")
            self.output_area.delete("1.0", "end")
            self.output_area.configure(state="disabled")

    def _bind_mousewheel(self, widget: ctk.CTkTextbox) -> None:
        """
        Binds mouse wheel events to enable scrolling in the specified widget.

        Parameters
        ----------
        widget : ctk.CTkTextbox
            The text widget to bind scrolling events to.

        Returns
        -------
            None
        """
        widget.bind("<MouseWheel>", lambda e: widget.yview_scroll(int(-1*(e.delta/120)), "units"))
        widget.bind("<Button-4>", lambda e: widget.yview_scroll(-1, "units"))  # Linux scroll up
        widget.bind("<Button-5>", lambda e: widget.yview_scroll(1, "units"))   # Linux scroll down

    def _unbind_mousewheel(self, widget: ctk.CTkTextbox) -> None:
        """
        Unbinds mouse wheel events from the specified widget.

        Parameters
        ----------
        widget : ctk.CTkTextbox
            The text widget to unbind scrolling events from.

        Returns
        -------
            None
        """
        widget.unbind("<MouseWheel>")
        widget.unbind("<Button-4>")
        widget.unbind("<Button-5>")
