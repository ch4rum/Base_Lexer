from Modules.Lexer_GUI import LexerGUI

if __name__ == "__main__":
    try:
        gui = LexerGUI()
        gui.run()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupción detectada (Ctrl+C). Cerrando la app...\n")
        if gui.status_bar:
            gui.status_bar.show_warning("Interrupted by user (Ctrl+C)")
        gui.exit()
