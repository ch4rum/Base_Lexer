from tkinter import filedialog, messagebox
import customtkinter as ctk

class FileHandler:
    """
    Handles file operations for the application including creating,
    opening, saving files, and managing file state changes.

    Attributes
    ----------
    current_open_file : str or None
        Path to the currently open file, or None if no file is open.
    content_init : str or None
        Initial content of the text area for change detection.
    text_areas : TextAreas or None
        Reference to the text areas component.
    text_area : CTkTextbox or None
        Reference to the main text input area.
    status_bar : StatusBar or None
        Reference to the status bar component.
    """
    def __init__(self):
        self.current_open_file = None
        self.content_init = None
        self.text_areas = None
        self.text_area = None
        self.status_bar = None

    def set_text_areas(self, text_areas: 'TextAreas') -> None:
        """
        Sets the reference to the text areas component and initializes
        the content tracking for change detection.

        Parameters
        ----------
        text_areas : TextAreas
            The text areas component containing input and output areas.

        Returns
        -------
            None
        """
        self.text_areas = text_areas
        self.text_area = self.text_areas.text_area
        if self.text_area:
            self.content_init = self.text_area.get("1.0", ctk.END).strip()

    def set_status_bar(self, status_bar: 'StatusBar') -> None:
        """
        Sets the reference to the status bar component for status updates.

        Parameters
        ----------
        status_bar : StatusBar
            The status bar component for displaying messages.

        Returns
        -------
            None
        """
        self.status_bar = status_bar

    def new_file(self):
        """
        Creates a new file by clearing the text area after checking
        if current changes should be saved.

        Returns
        -------
            None
        """
        if not self.text_area.get("1.0", ctk.END).strip() or self.save_check():
            self.text_area.delete("1.0", ctk.END)
            self.current_open_file = None
            self.content_init = self.text_area.get("1.0", ctk.END).strip()
            if self.status_bar:
                self.status_bar.set_text("New file created")
            self.text_areas.clear_output()

    def open_file(self):
        """
        Opens a file through a dialog, loading its content into the
        text area after checking for unsaved changes.

        Returns
        -------
            None
        """
        if not self.text_area.get("1.0", ctk.END).strip() or self.save_check():
            self.current_open_file = filedialog.askopenfilename(
                filetypes=[("Go files", "*.go"), ("TXT files", "*.txt"), ("All files", "*.*")]
            )
            if self.current_open_file:
                try:
                    self.text_area.delete("1.0", ctk.END)
                    with open(self.current_open_file, 'r') as f:
                        self.text_area.insert("1.0", f.read())
                    self.content_init = self.text_area.get("1.0", ctk.END).strip()
                    self.text_areas.clear_output()
                except Exception as e:
                    error_msg = f"Can't open file: {str(e)}"
                    messagebox.showerror("Error", error_msg)
                    if self.status_bar:
                        self.status_bar.show_error(error_msg)

    def save_check(self) -> bool:
        """
        Checks if there are unsaved changes and prompts the user to
        save before proceeding with destructive operations.

        Returns
        -------
        bool
            True if the operation can proceed, False if cancelled.
        """
        if not self.text_area:
            return True
        current_content = self.text_area.get("1.0", ctk.END).strip()
        if not current_content:
            return True
        if current_content != self.content_init:
            rta = messagebox.askyesnocancel(
                "Changes detected", "Do you want to save the changes?", icon="warning"
            )
            if rta is None:
                return False
            elif rta:
                self.save_file()
            return True
        return True

    def save_file(self):
        """
        Saves the current content to file, either overwriting the
        existing file or prompting for a new filename.

        Returns
        -------
            None
        """
        message = "There isn't content to save."
        if not self.text_area:
            messagebox.showinfo("Nothing to save", message)
            if self.status_bar:
                self.status_bar.show_info(message)
            return
        current_content = self.text_area.get("1.0", ctk.END).strip()
        if not current_content and not self.current_open_file:
            messagebox.showinfo("Nothing to save", message)
            if self.status_bar:
                self.status_bar.show_info(message)
            return
        message = "No changes detected to save."
        if current_content == self.content_init:
            messagebox.showinfo("No changes", message)
            if self.status_bar:
                self.status_bar.show_info(message)
            return
        if not self.current_open_file:
            new_filename = filedialog.asksaveasfilename(
                defaultextension=".go",
                filetypes=[("Go files", "*.go"), ("TXT files", "*.txt"), ("All files", "*.*")]
            )
            if new_filename:
                self.current_open_file = new_filename
            else:
                return
        try:
            with open(self.current_open_file, "w") as f:
                f.write(current_content)
            self.content_init = current_content
            if self.status_bar:
                self.status_bar.set_text(f"Save file: {self.current_open_file}")
        except Exception as e:
            error_msg = f"Unable to save the file:\n{str(e)}"
            messagebox.showerror("Save Error", error_msg)
            if self.status_bar:
                self.status_bar.show_error(error_msg)
