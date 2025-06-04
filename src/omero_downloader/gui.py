"""Main GUI application."""

import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import ttkbootstrap as ttk
import threading
import os
from pathlib import Path

from .utils import extract_datatype_and_ids


class OmeroDownloaderApp:
    """A GUI application for downloading data from OMERO."""

    def __init__(self, root):
        """Initialize the OmeroDownloaderApp.

        Parameters
        ----------
        root : tk.Tk
            The root window for the Tkinter application.
        """
        self.root = root
        self.root.title("OMERO Downloader")
        self.current_process = None
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.close_after_download = False
        self.skip_queue = False
        self.create_widgets()

    def create_widgets(self):
        """Create and layout the GUI widgets."""

        self.create_label("Download queue:  \n Enter URL or comma-separated IDs")
        self.queue_entry = self.create_entry(width=50)

        self.create_label(
            "For comma-Seperated IDs: \n "
            "Select data type: Project(s), Dataset(s) or Image(s)"
        )
        self.data_type_combobox = self.create_combobox(
            ["Project", "Dataset", "Image"], "Dataset", width=8
        )

        self.create_label("Enter storage path:")
        self.create_button("Browse", self.browse_dir)
        self.path_entry = self.create_entry(width=50, default_value="D:\\Data")

        self.create_label("Enter server address:")
        self.server_entry_combobox = self.create_combobox(
            ["omero.biozentrum.unibas.ch", "omero-nccr.biozentrum.unibas.ch"],
            "omero.biozentrum.unibas.ch",
            width=28,
        )

        self.create_label("Enter username:")
        self.username_entry = self.create_entry(width=50)
        self.populate_username()

        self.create_label("Enter password:")
        self.password_entry = self.create_entry(width=50, show="*")

        self.progress_label = tk.Label(self.root, text="", fg="blue")
        self.progress_label.pack(pady=10)

        self.create_button("Download all Images", self.start_download_thread)
        self.create_button("Skip remaining queue", self.skip_queued_downloads)

    def create_label(self, text):
        """Create a label widget.

        Parameters
        ----------
        text : str
            The text to display on the label.
        """
        label = tk.Label(self.root, text=text)
        label.pack(pady=10)

    def create_entry(self, width, default_value=None, show=None):
        """Create an entry widget.

        Parameters
        ----------
        width : int
            The width of the entry widget.
        default_value : str, optional
            The default value to insert into the entry (default is None).
        show : str, optional
            The character to display for password entry (default is None).

        Returns
        -------
        tk.Entry
            The created entry widget.
        """
        entry = tk.Entry(self.root, width=width, show=show)
        entry.pack(pady=10)
        if default_value:
            entry.insert(0, default_value)
        return entry

    def create_combobox(self, values, default_value, width):
        """Create a combobox widget.

        The combobox widget combines a text field with a pop-down list of values.

        Parameters
        ----------
        values : list of str
            The list of values for the combobox.
        default_value : str
            The default value to set in the combobox.
        width: int
            The width value, passed directly to the combobox widget.

        Returns
        -------
        ttk.Combobox
            The created combobox widget.
        """
        combobox = ttk.Combobox(self.root, values=values)
        combobox.set(default_value)
        combobox.configure(width=width)
        combobox.pack(pady=10)
        return combobox

    def create_button(self, text, command):
        """Create a button widget.

        Parameters
        ----------
        text : str
            The text to display on the button.
        command : callable
            The function to call when the button is clicked.
        """
        button = tk.Button(self.root, text=text, command=command)
        button.pack(pady=20)

    def start_download_thread(self):
        """Start the download process in a separate thread.

        Also resets all flags.
        """
        self.close_after_download = False
        self.skip_queue = False
        threading.Thread(target=self.run_script).start()

    def run_script(self):
        """Run the download script for the specified data."""

        server_address = self.server_entry_combobox.get()
        if str(server_address) in self.queue_entry.get():
            data_type, data_id = extract_datatype_and_ids(self.queue_entry.get())
        else:
            data_type = self.data_type_combobox.get()
            data_id = self.queue_entry.get().split(",")
            data_id = [obj_id.strip() for obj_id in data_id]

        storage_path = self.path_entry.get().strip().replace("\\", "/")
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        local_dir = Path(__file__).resolve().parent

        base_command = (
            f"download-pdi {{}}:{{}} "
            f'"{storage_path}" "{server_address}" "{username}" "{password}"'
        )

        for index, obj_id in enumerate(data_id):
            if self.close_after_download:
                self.root.destroy()
            if self.skip_queue:
                print(f"skipping ID {obj_id}")
                continue
            if isinstance(data_type, str):
                self.process_id(base_command, data_type, obj_id)
            if isinstance(data_type, list):
                self.process_id(base_command, data_type[index], obj_id)
            else:
                print(f"Unexpected Data type format {type(data_type)}")

        messagebox.showinfo("Complete", "Download of all data is completed.")

    def process_id(self, base_command, data_type, obj_id):
        """Process a Project, Dataset or Image ID for downloading.

        This method formats the base command with the data id, updates the progress label,
        and executes the command to download the data. It handles errors and updates the progress
        label accordingly.

        Parameters
        ----------
        base_command : str
            The base command to execute for downloading.
        data_type : str
            The type of data being processed (e.g., Project, Dataset, Image).
        obj_id : str
            The specific data id to download.
        """
        command = base_command.format(data_type, obj_id)
        self.update_progress_label(f"Processing {data_type}: {obj_id}")

        try:
            self.current_process = subprocess.Popen(command, shell=True)
            self.current_process.wait()
        except subprocess.CalledProcessError as e:
            self.show_error(f"Failed to download: {obj_id}\n{e}")
        except Exception as e:
            self.show_error(str(e))
        finally:
            self.current_process = None
            self.update_progress_label("")

    def update_progress_label(self, text):
        """Update the progress label with the given text.

        Parameters
        ----------
        text : str
            The text to display in the progress label.
        """
        self.progress_label.config(text=text)

    def show_error(self, message):
        """Display an error message in a message box.

        Parameters
        ----------
        message : str
            The error message to display.
        """
        messagebox.showerror("Error", message)

    def on_closing(self):
        """Handle the event when the window is closed.

        This method is called when the user attempts to close the GUI.
        It sets a flag to indicate that the user wants to close the application
        after the current download is finished.
        """
        if self.current_process:
            self.close_after_download = True
            messagebox.showinfo(
                "Download in Progress",
                "Please wait for the current download to finish.\n"
                "The App will then close automatically.",
            )
        else:
            self.root.destroy()

    def skip_queued_downloads(self):
        """Skip all queued downloads.

        The download of all file(s) associated to the currently
        processed ID will finish.
        """
        if self.current_process:
            self.skip_queue = True
            messagebox.showinfo(
                "Download in Progress",
                "Please wait for the current download to finish.\n"
                "All other downloads will be skipped.",
            )

    def browse_dir(self):
        """Browse for a directory and set it to the path entry."""
        path = filedialog.askdirectory()
        if path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, path)

    def populate_username(self):
        """Pre-populate the username field from the logged in user."""
        username = os.getlogin()
        self.username_entry.insert(0, username)
