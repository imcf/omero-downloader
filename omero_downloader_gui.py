import subprocess
import tkinter as tk
from tkinter import messagebox, ttk
import threading

# Global variable to keep track of the current process
current_process = None

def run_script():
    global current_process
    dataset_type = dataset_type_combobox.get()  # Get the selected dataset type
    dataset_numbers = entry.get().split(',')
    storage_path = path_entry.get().strip()  # Get the user-defined storage path
    storage_path = storage_path.replace("\\", "/")
    base_command = f'python C:/Tools/omero-downloader/download_pdi.py {dataset_type}:{{}} "{storage_path}"'
    
    for number in dataset_numbers:
        number = number.strip()  # Remove any extra spaces
        command = base_command.format(number)
        
        # Update the progress label in the GUI
        progress_label.config(text=f"Processing {dataset_type}: {number}")
        
        try:
            # Start the command in a separate thread
            current_process = subprocess.Popen(command, shell=True)
            current_process.wait()  # Wait for the process to complete
            messagebox.showinfo("Success", f"Executed: {command}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to execute: {command}\n{e}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            current_process = None
            progress_label.config(text="")  # Clear the progress label after completion

    # Show a completion message after all datasets/projects have been processed
    messagebox.showinfo("Complete", f"All {dataset_type}s have been processed.")

def cancel_script():
    global current_process
    if current_process:
        current_process.terminate()  # Terminate the running process
        messagebox.showinfo("Cancelled", "The process has been cancelled.")
        current_process = None
        progress_label.config(text="")  # Clear the progress label on cancel

# Create the main window
root = tk.Tk()
root.title("Dataset Runner")

# Create and place the label for dataset type selection
label_type = tk.Label(root, text="Select type (Dataset or Project):")
label_type.pack(pady=10)

# Create a combobox for selecting dataset type
dataset_type_combobox = ttk.Combobox(root, values=["Dataset", "Project"])
dataset_type_combobox.set("Dataset")  # Set default value
dataset_type_combobox.pack(pady=10)

# Create and place the input field for dataset numbers
label_numbers = tk.Label(root, text="Enter dataset numbers (comma-separated):")
label_numbers.pack(pady=10)

entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Create and place the label for storage path
label_path = tk.Label(root, text="Enter storage path:")
label_path.pack(pady=10)

# Create an input field for the storage path
path_entry = tk.Entry(root, width=50)
path_entry.pack(pady=10)
path_entry.insert(0, "D:\\Data")  # Set default value

# Create and place the progress label
progress_label = tk.Label(root, text="", fg="blue")
progress_label.pack(pady=10)

# Create and place the run button
run_button = tk.Button(root, text="Run Script", command=lambda: threading.Thread(target=run_script).start())
run_button.pack(pady=20)

# Create and place the cancel button
cancel_button = tk.Button(root, text="Cancel", command=cancel_script)
cancel_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()
