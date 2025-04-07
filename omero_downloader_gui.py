import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import threading

# Global variable to keep track of the current process
current_process = None

def run_script():
    global current_process
    dataset_type = dataset_type_combobox.get()
    dataset_numbers = entry.get().split(',')
    storage_path = path_entry.get().strip()
    storage_path = storage_path.replace("\\", "/")
    server_address = server_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip() 

    base_command = f'python C:/Tools/omero-downloader/download_pdi.py {dataset_type}:{{}} "{storage_path}" "{server_address}" "{username}" "{password}"'
    
    for number in dataset_numbers:
        number = number.strip()  # Remove extra spaces
        command = base_command.format(number)
        
        # Update the progress label in the GUI
        progress_label.config(text=f"Processing {dataset_type}: {number}")
        
        try:
            # Start the command in a separate thread
            current_process = subprocess.Popen(command, shell=True)
            current_process.wait()  # Wait for the process to complete
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to download: {number}\n{e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            current_process = None
            progress_label.config(text="")  # Clear the progress label after completion

    messagebox.showinfo("Complete", f"Download of all {dataset_type}s is completed.")


def cancel_script():
    global current_process
    if current_process:
        current_process.terminate()
        messagebox.showinfo("Cancelled", "The current download has been cancelled.")
        current_process = None
        progress_label.config(text="")  # Clear the progress label on cancel


# Create the main GUI window
root = tk.Tk()
root.title("OMERO Downloader")

label_type = tk.Label(root, text="Select type: Project(s), Dataset(s) or Image(s)")
label_type.pack(pady=10)

dataset_type_combobox = ttk.Combobox(root, values=["Project", "Dataset", "Image"])
dataset_type_combobox.set("Dataset")
dataset_type_combobox.pack(pady=10)

label_numbers = tk.Label(root, text="Enter IDs (comma-separated):")
label_numbers.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

label_path = tk.Label(root, text="Enter storage path:")
label_path.pack(pady=10)

path_entry = tk.Entry(root, width=50)
path_entry.pack(pady=10)
path_entry.insert(0, "D:\\Data")

label_server = tk.Label(root, text="Enter server address:")
label_server.pack(pady=10)

server_entry = tk.Entry(root, width=50)
server_entry.pack(pady=10)
server_entry.insert(0, "omero.biozentrum.unibas.ch")

label_username = tk.Label(root, text="Enter username:")
label_username.pack(pady=10)

username_entry = tk.Entry(root, width=50)
username_entry.pack(pady=10)

label_password = tk.Label(root, text="Enter password:")
label_password.pack(pady=10)

password_entry = tk.Entry(root, width=50, show="*")  # Use show="*" to hide the password
password_entry.pack(pady=10)

progress_label = tk.Label(root, text="", fg="blue")
progress_label.pack(pady=10)

run_button = tk.Button(root, text="Download all", command=lambda: threading.Thread(target=run_script).start())
run_button.pack(pady=20)

cancel_button = tk.Button(root, text="Cancel current download", command=cancel_script)
cancel_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
