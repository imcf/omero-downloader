import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import threading


class OmeroDownloaderApp:
    """A GUI application for downloading datasets from OMERO."""

    def __init__(self, root):
        """
        Initialize the OmeroDownloaderApp.

        Parameters
        ----------
        root : tk.Tk
            The root window for the Tkinter application.
        """
        self.root = root
        self.root.title("OMERO Downloader")
        self.current_process = None

        self.create_widgets()


    def create_widgets(self):
        """Create and layout the GUI widgets."""

        self.create_label("Select type: Project(s), Dataset(s) or Image(s)")
        self.dataset_type_combobox = self.create_combobox(["Project", "Dataset", "Image"], "Dataset")
        self.create_label("Enter IDs (comma-separated):")
        self.entry = self.create_entry(width=50)
        self.create_label("Enter storage path:")
        self.path_entry = self.create_entry(width=50, default_value="D:\\Data")
        self.create_label("Enter server address:")
        self.server_entry = self.create_entry(width=50, default_value="omero.biozentrum.unibas.ch")
        self.create_label("Enter username:")
        self.username_entry = self.create_entry(width=50)
        self.create_label("Enter password:")
        self.password_entry = self.create_entry(width=50, show="*")

        self.progress_label = tk.Label(self.root, text="", fg="blue")
        self.progress_label.pack(pady=10)

        self.create_button("Download all Images", self.start_download_thread)
        self.create_button("Cancel current download", self.cancel_script)


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


    def create_combobox(self, values, default_value):
        """Create a combobox widget.
        The combobox widget combines a text field with a pop-down list of values.

        Parameters
        ----------
        values : list of str
            The list of values for the combobox.
        default_value : str
            The default value to set in the combobox.

        Returns
        -------
        ttk.Combobox
            The created combobox widget.
        """
        combobox = ttk.Combobox(self.root, values=values)
        combobox.set(default_value)
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
        """Start the download process in a separate thread."""

        threading.Thread(target=self.run_script).start()


    def run_script(self):
        """Run the download script for the specified datasets."""

        dataset_type = self.dataset_type_combobox.get()
        dataset_numbers = self.entry.get().split(',')
        storage_path = self.path_entry.get().strip().replace("\\", "/")
        server_address = self.server_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        base_command = f'python C:/Tools/omero-downloader/download_pdi.py {dataset_type}:{{}} "{storage_path}" "{server_address}" "{username}" "{password}"'

        for number in map(str.strip, dataset_numbers):
            self.process_dataset_number(base_command, dataset_type, number)

        messagebox.showinfo("Complete", f"Download of all {dataset_type}s is completed.")


    def process_dataset_number(self, base_command, dataset_type, number):
        """Process a single dataset ID for downloading.

        This method formats the base command with the dataset number, updates the progress label,
        and executes the command to download the dataset. It handles errors and updates the progress
        label accordingly.

        Parameters
        ----------
        base_command : str
            The base command to execute for downloading.
        dataset_type : str
            The type of dataset being processed (e.g., Project, Dataset, Image).
        number : str
            The specific dataset number to download.
        """
        command = base_command.format(number)
        self.update_progress_label(f"Processing {dataset_type}: {number}")

        try:
            self.current_process = subprocess.Popen(command, shell=True)
            self.current_process.wait()
        except subprocess.CalledProcessError as e:
            self.show_error(f"Failed to download: {number}\n{e}")
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


    def cancel_script(self):
        """Cancel the current download process.

        This method terminates the current download process if it is running and updates
        the progress label accordingly. It also shows a message box to inform the user
        that the download has been cancelled.
        """
        if self.current_process:
            self.current_process.terminate()
            messagebox.showinfo("Cancelled", "The current download has been cancelled.")
            self.current_process = None
            self.update_progress_label("")


if __name__ == "__main__":
    root = tk.Tk()
    app = OmeroDownloaderApp(root)
    root.mainloop()
