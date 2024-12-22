import json
import tkinter as tk
from tkinter import filedialog
from ttkbootstrap import Style

def read_json_file():
    """Prompt user to select a JSON file and return its content as a dictionary."""
    file_path = filedialog.askopenfilename(
        title="Select JSON File",
        filetypes=[("JSON Files", "*.json")]
    )
    if not file_path:
        return None

    try:
        with open(file_path, 'r') as file:
            return json.load(file), file_path
    except Exception as e:
        log_text.set(f"Error reading file: {e}")
        return None

def convert_to_markdown(data):
    """Convert a nested dictionary to Markdown format."""
    def process_dict(d, level=1):
        md = ""
        for key, value in d.items():
            md += f"{'#' * level} {key}\n\n"
            if isinstance(value, dict):
                md += process_dict(value, level + 1)
            elif isinstance(value, list):
                for item in value:
                    md += f"- {item}\n"
                md += "\n"
            else:
                md += f"{value}\n\n"
        return md

    return process_dict(data)

def save_to_md_file(md_content):
    """Save the Markdown content to a .md file."""
    file_path = filedialog.asksaveasfilename(
        title="Save Markdown File",
        defaultextension=".md",
        filetypes=[("Markdown Files", "*.md")]
    )
    if not file_path:
        return

    try:
        with open(file_path, 'w') as file:
            file.write(md_content)
        log_text.set(f"Markdown saved to {file_path}")
    except Exception as e:
        log_text.set(f"Error saving file: {e}")

def process_json_to_markdown():
    """Read JSON file, convert to Markdown, and display content."""
    result = read_json_file()
    if result is None:
        return

    json_data, file_path = result
    try:
        markdown_content = convert_to_markdown(json_data)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, markdown_content)
        log_text.set(f"Converted JSON from {file_path} to Markdown.")

        save_to_md_file(markdown_content)
    except Exception as e:
        log_text.set(f"Error processing JSON: {e}")

# GUI Setup
style = Style(theme="darkly")
root = style.master
root.title("JSON to Markdown Converter")

# Widgets
frame = tk.Frame(root, padx=10, pady=10)
frame.pack(fill="both", expand=True)

log_text = tk.StringVar()
log_text.set("Select a JSON file to start.")

log_label = tk.Label(frame, textvariable=log_text, wraplength=400, fg="blue")
log_label.pack(pady=5)

convert_button = tk.Button(frame, text="Convert JSON to Markdown", command=process_json_to_markdown)
convert_button.pack(pady=10)

output_text = tk.Text(frame, wrap="word", height=20, width=80)
output_text.pack(pady=5, fill="both", expand=True)

# Main loop
root.mainloop()
