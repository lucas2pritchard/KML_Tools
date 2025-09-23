import os
import importlib
import tkinter as tk
from tkinter import filedialog, messagebox
import simplekml

def select_directory():
    folder_path = filedialog.askdirectory(title="Select Folder")
    if folder_path:
        directory_label.config(text=f"Selected Directory: {folder_path}")
        populate_kml_files(folder_path)

def populate_kml_files(folder_path):
    kml_files = [f for f in os.listdir(folder_path) if f.endswith(".kml")]
    kml_dropdown['menu'].delete(0, 'end')
    for kml in kml_files:
        kml_dropdown['menu'].add_command(label=kml, command=lambda value=kml: kml_variable.set(value))
    if kml_files:
        kml_variable.set(kml_files[0])
    else:
        kml_variable.set("No KML files found")

def load_edit_functions():
    """Load available editing functions from the lib folder."""
    lib_path = os.path.join(os.path.dirname(__file__), 'lib')
    function_files = [f[:-3] for f in os.listdir(lib_path) if f.endswith(".py") and f != "__init__.py"]
    function_dropdown['menu'].delete(0, 'end')
    for func in function_files:
        function_dropdown['menu'].add_command(label=func, command=lambda value=func: function_variable.set(value))
    if function_files:
        function_variable.set(function_files[0])
    else:
        function_variable.set("No functions available")

def edit_kml_file():
    directory = directory_label.cget("text").replace("Selected Directory: ", "")
    kml_file = kml_variable.get()
    selected_function = function_variable.get()

    if not directory or not kml_file or kml_file == "No KML files found" or not selected_function:
        messagebox.showerror("Error", "Please select a valid directory, KML file, and function.")
        return

    kml_path = os.path.join(directory, kml_file)

    try:
        lib_module = importlib.import_module(f'lib.{selected_function}')
        edit_function = getattr(lib_module, 'edit_kml')  # Assuming each script has an 'edit_kml' function
        edit_function(kml_path)

        messagebox.showinfo("Success", f"Edited KML file: {kml_file} using {selected_function}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to edit KML file: {e}")

# Create the main window
root = tk.Tk()
root.title("KML File Editor")

# Select Directory Button
directory_label = tk.Label(root, text="Selected Directory: None", wraplength=400)
directory_label.pack(pady=10)

select_dir_button = tk.Button(root, text="Select Directory", command=select_directory)
select_dir_button.pack(pady=5)

# KML File Dropdown
kml_variable = tk.StringVar(root)
kml_variable.set("No KML files found")

kml_dropdown = tk.OptionMenu(root, kml_variable, "No KML files found")
kml_dropdown.pack(pady=5)

# Function Dropdown
function_variable = tk.StringVar(root)
function_variable.set("No functions available")

function_dropdown = tk.OptionMenu(root, function_variable, "No functions available")
function_dropdown.pack(pady=5)

# Load functions from lib
load_edit_functions()

# Edit Button
edit_button = tk.Button(root, text="Edit KML File", command=edit_kml_file)
edit_button.pack(pady=10)

# Run the main loop
root.mainloop()