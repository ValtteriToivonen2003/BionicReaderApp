import tkinter as tk
from tkinter import filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES
import os
from tkinter import filedialog

from theme_manager import LIGHT, DARK, apply_theme
from file_handler import extract_text
from bionic_formatter import bionic_read
from fpdf import FPDF

# Theme toggle setup
current_theme = DARK

def toggle_theme():
    global current_theme
    current_theme = DARK if current_theme == LIGHT else LIGHT
    apply_theme(root, [label, button, toggle_button], current_theme)

# Save formatted text to PDF
def save_to_pdf(formatted_lines):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for line in formatted_lines:
        for text, is_bold in line:
            style = 'B' if is_bold else ''
            pdf.set_font("Arial", style=style, size=12)
            
            # Encode text to latin-1, replacing unsupported characters
            encoded_text = text.encode('latin-1', 'replace').decode('latin-1')
            pdf.write(h=10, txt=encoded_text)
        pdf.ln() # Move to the next line after processing a line
    
    # Save to the Downloads folder and open it
    downloads_path = os.path.join(os.path.expanduser('~'), 'Downloads', 'output.pdf')
    pdf.output(downloads_path)
    os.startfile(downloads_path)

# Handle file drop
def handle_drop(event):
    path = event.data.strip('{}')  
    try:
        raw_text = extract_text(path)  
        formatted_text = bionic_read(raw_text)
        save_to_pdf(formatted_text)
        label.config(text="File processed and saved to PDF.")
    except Exception as e:
        label.config(text=f"Error: {str(e)}")

# Initialize GUI
root = TkinterDnD.Tk()  
root.title("Bionic Reader")
root.geometry("400x300")  

label = tk.Label(root, text="Drag and drop your file here", width=40, height=10)  
label.pack(pady=20)  
label.drop_target_register(DND_FILES)  
label.dnd_bind('<<Drop>>', handle_drop)  

# New button for file picker
def pick_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            raw_text = extract_text(file_path)
            formatted_text = bionic_read(raw_text)
            save_to_pdf(formatted_text)
            label.config(text="File processed and saved to PDF.")
        except Exception as e:
            label.config(text=f"Error: {str(e)}")

file_picker_button = tk.Button(root, text="Find file you want to use", command=pick_file)
file_picker_button.pack(pady=10)

button = tk.Button(root, text="Process File", command=lambda: label.config(text="Drop a file to begin"))
button.pack(pady=10)

toggle_button = tk.Button(root, text="Toggle Theme", command=toggle_theme)
toggle_button.pack(pady=10)

apply_theme(root, [label, button, toggle_button, file_picker_button], current_theme)

root.mainloop()
