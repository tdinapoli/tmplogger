import random
import threading
import logging
import tkinter as tk
from tkinter import ttk
import sys
import pathlib

from logging_config import get_temperature_logger, init_logging_config, init_logging_dirs
from mercury_itc import MercuryiTC
import pyvisa
import sv_ttk


def query_dummy():
    return random.random()


class GuiLogger(logging.Handler):
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.text_widget.configure(state=tk.DISABLED)

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg + '\n')
        self.text_widget.configure(state=tk.DISABLED)
        self.text_widget.see(tk.END)

class App:
    def __init__(self, root, path: pathlib.Path):
        self.root = root
        self.root.title("Instrument Temperature Logger")
        logging.info("Opening the program")

        # Logger setup
        self.logger = get_temperature_logger(path)
        self.timer = None

        # Layout
        self.setup_ui()

        # Mercury Instrument
        self.mercury = None
        self.is_logging = False

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def setup_ui(self):
        # Port selection
        self.port_label = ttk.Label(self.root, text="Select Port:")
        self.port_label.grid(row=0, column=0, padx=10, pady=10)

        self.port_combobox = ttk.Combobox(self.root, values=self.get_available_ports(), state="readonly")
        self.port_combobox.grid(row=0, column=1, padx=10, pady=10)

        # Logging button
        self.toggle_button = ttk.Button(self.root, text="Toggle Logging", command=self.toggle_logging)
        self.toggle_button.grid(row=0, column=2, padx=10, pady=10)

        # Status label
        self.status_label = ttk.Label(self.root, text="Status: Stopped", foreground="red")
        self.status_label.grid(row=2, column=0, columnspan=3, pady=10)

        # Configure grid resizing
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def get_available_ports(self):
        # Detect available ports using pyvisa
        try:
            rm = pyvisa.ResourceManager('@py')
            return rm.list_resources()
        except Exception as e:
            raise

    def toggle_logging(self):
        if self.is_logging:
            self.stop_logging()
            self.toggle_button.config(text="Log", style="TButton")
            self.status_label.config(text="Status: Stopped", foreground="red")
            logging.info("Logging stopped.")
        else:
            port = self.port_combobox.get()
            if not port:
                logging.error("No port selected.")
                raise ValueError("No port selected.")
            try:
                if not self.mercury:
                    self.mercury = MercuryiTC(port = port)
                self.toggle_button.config(text="Stop", style="TButton")
                self.toggle_button.configure(style="Active.TButton")
                self.status_label.config(text="Status: Logging...", foreground="green")
                logging.info("Logger started.")
                self.run(self.mercury.query_temperature)
            except Exception as e:
                raise Exception(e)

    def log_tmp(self, query_fn):
        tmp = query_fn()
        self.logger.info(f"{tmp}")


    def run(self, query_fn):
        self.log_tmp(query_fn)
        self.timer = threading.Timer(5.0, lambda: self.run(query_fn))
        self.timer.start()
        self.is_logging = True

    def stop_logging(self):
        self.is_logging = False
        if self.timer is not None:
            self.timer.cancel()

    def close_window(self):
        """
        Gracefully stop the program when the window is closed.
        """
        logging.info("Shutting down the program...")
        self.stop_logging()
        self.root.destroy()  # Destroy the Tkinter window
        sys.exit(0)  # Exit the program completely

def main():
    ROOT = pathlib.Path(
        r"C:\Users\Public\templogger"
    )
    init_logging_dirs(ROOT)    
    init_logging_config(ROOT)
    root_tk = tk.Tk()
    app = App(root_tk, path=ROOT)
    sv_ttk.set_theme('dark')
    root_tk.mainloop()

if __name__ == "__main__":
    main()
