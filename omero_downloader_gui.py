import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import threading


class OmeroDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("OMERO Downloader")
        self.current_process = None

        self.create_widgets()


    def create_widgets(self):
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

        self.create_button("Download all", self.start_download_thread)
        self.create_button("Cancel current download", self.cancel_script)


    def create_label(self, text):
        label = tk.Label(self.root, text=text)
        label.pack(pady=10)


    def create_entry(self, width, default_value=None, show=None):
        entry = tk.Entry(self.root, width=width, show=show)
        entry.pack(pady=10)
        if default_value:
            entry.insert(0, default_value)
        return entry


    def create_combobox(self, values, default_value):
        combobox = ttk.Combobox(self.root, values=values)
        combobox.set(default_value)
        combobox.pack(pady=10)
        return combobox


    def create_button(self, text, command):
        button = tk.Button(self.root, text=text, command=command)
        button.pack(pady=20)


    def start_download_thread(self):
        threading.Thread(target=self.run_script).start()


    def run_script(self):
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
        self.progress_label.config(text=text)


    def show_error(self, message):
        messagebox.showerror("Error", message)


    def cancel_script(self):
        if self.current_process:
            self.current_process.terminate()
            messagebox.showinfo("Cancelled", "The current download has been cancelled.")
            self.current_process = None
            self.update_progress_label("")


if __name__ == "__main__":
    root = tk.Tk()
    app = OmeroDownloaderApp(root)
    root.mainloop()
