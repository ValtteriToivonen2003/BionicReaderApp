import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from tkinterdnd2 import TkinterDnD, DND_FILES
import os

from theme_manager import LIGHT, DARK, apply_theme
from file_handler import extract_text
from bionic_formatter import bionic_read
from fpdf import FPDF

# Global state
current_theme = DARK  # Start with dark theme by default
current_formatted_result = None

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
root.geometry("1200x800")  

# Configure grid weights for responsive layout
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

# Frame for buttons
button_frame = tk.Frame(root)
button_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Drop zone label
label = tk.Label(button_frame, text="Drag and drop your file here")
label.pack(side=tk.LEFT, padx=5)
label.drop_target_register(DND_FILES)
label.dnd_bind('<<Drop>>', handle_drop)

# Create left and right frames for text areas
left_frame = tk.LabelFrame(root, text="Original Text")
left_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

right_frame = tk.LabelFrame(root, text="Bionic Reading Format")
right_frame.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

# Configure frame grid weights
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_columnconfigure(0, weight=1)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

# Original text display area
original_text = scrolledtext.ScrolledText(left_frame, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
original_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Formatted text display area
formatted_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD, width=50, height=20, font=("Arial", 12))
formatted_text.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

def display_text(raw_text, formatted_result):
    # Display original text
    original_text.delete('1.0', tk.END)
    original_text.insert(tk.END, raw_text)
    
    # Display formatted text
    formatted_text.delete('1.0', tk.END)
    formatted_text.tag_configure("bold", font=("Arial", 12, "bold"))
    
    for line in formatted_result:
        for text, is_bold in line:
            if is_bold:
                formatted_text.insert(tk.END, text, "bold")
            else:
                formatted_text.insert(tk.END, text)
        formatted_text.insert(tk.END, '\n')

def update_status(message):
    label.config(text=message)
    root.update_idletasks()

def save_to_pdf_with_name():
    global current_formatted_result
    if current_formatted_result is None:
        update_status("No formatted text available. Please open a file first.")
        return

    file_path = filedialog.asksaveasfilename(
        initialdir=os.path.join(os.path.expanduser('~'), 'Downloads'),
        title="Save PDF as",
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )
    if file_path:
        try:
            pdf = FPDF()
            pdf.add_page()
            
            # Set up PDF with Arial font
            pdf.set_font("Arial", size=12)
            
            for line in current_formatted_result:
                for text, is_bold in line:
                    style = 'B' if is_bold else ''
                    pdf.set_font("Arial", style=style, size=12)
                    
                    # Replace smart quotes with regular quotes
                    text = text.replace('"', '"').replace('"', '"')
                    text = text.replace(''', "'").replace(''', "'")
                    
                    # Handle other special characters
                    text = text.replace('–', '-').replace('—', '-')  # Replace em/en dashes
                    text = text.replace('…', '...') # Replace ellipsis
                    
                    # Encode to latin-1, replacing any remaining unsupported characters
                    text = text.encode('latin-1', 'replace').decode('latin-1')
                    
                    # Write the text
                    pdf.write(h=10, txt=text)
                pdf.ln()  # New line after each complete line                
            pdf.output(file_path)
            update_status(f"File saved successfully to {file_path}")
        except Exception as e:
            update_status(f"Error saving PDF: {str(e)}")

# Update handle_drop function
def handle_drop(event):
    global current_formatted_result
    path = event.data.strip('{}')
    try:
        update_status("Processing file...")
        raw_text = extract_text(path)
        formatted_result = bionic_read(raw_text)
        current_formatted_result = formatted_result  # Store the formatted result
        display_text(raw_text, formatted_result)
        update_status("File processed. Click 'Save as PDF' to download.")
    except Exception as e:
        current_formatted_result = None
        update_status(f"Error: {str(e)}")

# New button for file picker
def pick_file():
    global current_formatted_result
    file_path = filedialog.askopenfilename(
        filetypes=[("Supported files", "*.pdf *.html *.htm")]
    )
    if file_path:
        try:
            update_status("Processing file...")
            raw_text = extract_text(file_path)
            formatted_result = bionic_read(raw_text)
            current_formatted_result = formatted_result  # Store the formatted result
            display_text(raw_text, formatted_result)
            update_status("File processed. Click 'Save as PDF' to download.")
        except Exception as e:
            current_formatted_result = None
            update_status(f"Error: {str(e)}")

# Control buttons frame
control_frame = tk.Frame(root)
control_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="ew")

# Add Save PDF button
save_button = tk.Button(control_frame, text="Save as PDF", command=save_to_pdf_with_name)
save_button.pack(side=tk.LEFT, padx=5)

file_picker_button = tk.Button(control_frame, text="Open File", command=pick_file)
file_picker_button.pack(side=tk.LEFT, padx=5)

toggle_button = tk.Button(control_frame, text="Toggle Theme", command=toggle_theme)
toggle_button.pack(side=tk.RIGHT, padx=5)

# Apply theme
apply_theme(root, [
    label, 
    file_picker_button, 
    toggle_button, 
    save_button,
    original_text,
    formatted_text,
    left_frame,
    right_frame
], current_theme)

root.mainloop()
