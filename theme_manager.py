


LIGHT = {
    "bg": "#e6f3f5",  # Light blue-gray background
    "fg": "#2c3e50",  # Dark blue-gray text
    "button_bg": "#bdd8dc",  # Slightly darker blue-gray for buttons
    "button_fg": "#2c3e50",  # Dark blue-gray text
    "text_bg": "#f5f9fa",  # Very light blue-gray for text area
    "text_fg": "#2c3e50",  # Dark blue-gray text
    "font": ("Arial", 12),
    "font_bold": ("Arial", 12, "bold")
}

DARK = {
    "bg": "#1a1f36",  # Deep blue-gray background
    "fg": "#e6f3f5",  # Light blue-gray text
    "button_bg": "#2d3655",  # Medium blue-gray for buttons
    "button_fg": "#e6f3f5",  # Light blue-gray text
    "text_bg": "#262f4d",  # Slightly lighter than bg for text area
    "text_fg": "#e6f3f5",  # Light blue-gray text
    "font": ("Arial", 12),
    "font_bold": ("Arial", 12, "bold")
}

def apply_theme(root, widgets, theme):
    root.configure(bg=theme["bg"])
    for widget in widgets:
        widget_str = str(widget)
        if widget_str.endswith('.!scrolledtext'):  # Text display widget
            widget.configure(
                bg=theme["text_bg"],
                fg=theme["text_fg"],
                insertbackground=theme["text_fg"],  # Cursor color
                relief="flat",
                borderwidth=1
            )
        elif widget_str.endswith('.!labelframe'):  # Frame widgets
            widget.configure(
                bg=theme["bg"],
                fg=theme["fg"],
                relief="groove",
                borderwidth=1
            )
        elif widget_str.endswith('.!button'):  # Buttons
            widget.configure(
                bg=theme["button_bg"],
                fg=theme["button_fg"],
                relief="raised",
                borderwidth=1
            )
        else:  # Other widgets (labels, etc)
            widget.configure(
                bg=theme["bg"],
                fg=theme["fg"]
            )