import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import xml.etree.ElementTree as ET
import os

def load_and_display_xml():
    # Open file dialog to select the XML file
    xml_file = filedialog.askopenfilename(
        title="Select MAVLink XML File",
        filetypes=(("XML Files", "*.xml"), ("All Files", "*.*"))
    )

    if not xml_file:
        return  # If no file is selected, return

    try:
        # Clear both Treeviews before loading new data
        tree_message.delete(*tree_message.get_children())
        tree_enum.delete(*tree_enum.get_children())
        description_label_message.config(text="")
        description_label_enum.config(text="")

        # Load the main XML and its includes
        base_path = os.path.dirname(xml_file)
        main_message_root_id = tree_message.insert("", "end", text=os.path.basename(xml_file), open=True)
        main_enum_root_id = tree_enum.insert("", "end", text=os.path.basename(xml_file), open=True)
        parse_and_load_xml(xml_file, base_path, main_message_root_id, main_enum_root_id)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to load XML file: {e}")

def parse_and_load_xml(xml_file, base_path, parent_message_root_id, parent_enum_root_id):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Handle includes by recursively loading and parsing them
    for include in root.findall('include'):
        included_file = include.text.strip()
        included_file_path = os.path.join(base_path, included_file)
        if os.path.exists(included_file_path):
            included_message_root_id = tree_message.insert(parent_message_root_id, "end", text=included_file, open=True)
            included_enum_root_id = tree_enum.insert(parent_enum_root_id, "end", text=included_file, open=True)
            parse_and_load_xml(included_file_path, base_path, included_message_root_id, included_enum_root_id)
        else:
            messagebox.showwarning("Warning", f"Included file '{included_file}' not found.")

    # Load Messages
    for msg in root.findall('messages/message'):
        name = msg.get('name')
        msg_id = msg.get('id')
        msg_desc = msg.find('description').text if msg.find('description') is not None else "No description available."
        parent_id = tree_message.insert(parent_message_root_id, "end", values=(name, msg_id))
        tree_message.set(parent_id, "Description", msg_desc)
        for field in msg.findall('field'):
            field_name = field.get('name')
            field_type = field.get('type')
            field_id = tree_message.insert(parent_id, "end", values=(field_name, field_type))
            field_desc = field.find('description').text if field.find('description') is not None else "No description available."
            tree_message.set(field_id, "Description", field_desc)

    # Load Enums
    for enum in root.findall('enums/enum'):
        name = enum.get('name')
        enum_desc = enum.find('description').text if enum.find('description') is not None else "No description available."
        parent_id = tree_enum.insert(parent_enum_root_id, "end", values=(name, ""))
        tree_enum.set(parent_id, "Description", enum_desc)
        for entry in enum.findall('entry'):
            entry_name = entry.get('name')
            entry_value = entry.get('value')
            entry_id = tree_enum.insert(parent_id, "end", values=(entry_name, entry_value))
            entry_desc = entry.find('description').text if entry.find('description') is not None else "No description available."
            tree_enum.set(entry_id, "Description", entry_desc)

def on_tree_select(event, tree, description_label):
    selected_item = tree.selection()[0]  # Get selected item
    description = tree.set(selected_item, "Description")  # Get the description from the "Description" field
    if not description:
        description = "No description available."
    description_label.config(text=f"Description:\n{description}")

# Create the main window
root = tk.Tk()
root.title("MAVLink Messages and Enums")

# Create a notebook (tabs) for messages and enums
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

# Create frames for each tab
frame_message = tk.Frame(notebook)
frame_enum = tk.Frame(notebook)

notebook.add(frame_message, text="Messages")
notebook.add(frame_enum, text="Enums")

# Create a button to select an XML file
button = tk.Button(root, text="Select XML File", command=load_and_display_xml)
button.pack(pady=10)

# Create the Treeview widget for Messages
tree_message_frame = tk.Frame(frame_message)
tree_message_frame.pack(expand=True, fill='both')

tree_scrollbar_message = ttk.Scrollbar(tree_message_frame)
tree_scrollbar_message.pack(side=tk.RIGHT, fill=tk.Y)

tree_message = ttk.Treeview(tree_message_frame, yscrollcommand=tree_scrollbar_message.set)
tree_scrollbar_message.config(command=tree_message.yview)

# Define the columns for Messages
tree_message["columns"] = ("Name", "ID", "Description")
tree_message.column("#0", width=300, minwidth=300)  # Adjust the width for the tree structure
tree_message.column("Name", anchor=tk.W, width=200)
tree_message.column("ID", anchor=tk.W, width=100)
tree_message.column("Description", width=0, minwidth=0, stretch=tk.NO)

# Define the column headings for Messages
tree_message.heading("Name", text="Name", anchor=tk.W)
tree_message.heading("ID", text="ID/Type", anchor=tk.W)

# Bind the tree selection event to a handler for Messages
tree_message.bind("<<TreeviewSelect>>", lambda event: on_tree_select(event, tree_message, description_label_message))
tree_message.pack(expand=True, fill='both', side=tk.LEFT)

# Create a label to display descriptions for Messages
description_label_message = tk.Label(frame_message, text="", wraplength=600, justify=tk.LEFT)
description_label_message.pack(pady=10, padx=10)

# Create the Treeview widget for Enums
tree_enum_frame = tk.Frame(frame_enum)
tree_enum_frame.pack(expand=True, fill='both')

tree_scrollbar_enum = ttk.Scrollbar(tree_enum_frame)
tree_scrollbar_enum.pack(side=tk.RIGHT, fill=tk.Y)

tree_enum = ttk.Treeview(tree_enum_frame, yscrollcommand=tree_scrollbar_enum.set)
tree_scrollbar_enum.config(command=tree_enum.yview)

# Define the columns for Enums
tree_enum["columns"] = ("Name", "ID", "Description")
tree_enum.column("#0", width=300, minwidth=300)  # Adjust the width for the tree structure
tree_enum.column("Name", anchor=tk.W, width=200)
tree_enum.column("ID", anchor=tk.W, width=100)
tree_enum.column("Description", width=0, minwidth=0, stretch=tk.NO)

# Define the column headings for Enums
tree_enum.heading("Name", text="Name", anchor=tk.W)
tree_enum.heading("ID", text="Value", anchor=tk.W)

# Bind the tree selection event to a handler for Enums
tree_enum.bind("<<TreeviewSelect>>", lambda event: on_tree_select(event, tree_enum, description_label_enum))
tree_enum.pack(expand=True, fill='both', side=tk.LEFT)

# Create a label to display descriptions for Enums
description_label_enum = tk.Label(frame_enum, text="", wraplength=600, justify=tk.LEFT)
description_label_enum.pack(pady=10, padx=10)

# Start the Tkinter event loop
root.mainloop()
