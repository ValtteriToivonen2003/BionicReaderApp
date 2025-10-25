


LIGHT = {
    "bg": 'white', 
    "fg": "black", 
    "button_bg": "lightgray",
    "button_fg": "black"
}

DARK = {
    "bg": "#2e2e2e",
    "fg": "white",
    "button_bg": "#444444",
    "button_fg": "white"
    }

def apply_theme(root, widgets, theme):
    root.configure(bg=theme["bg"])
    for widget in widgets:
        widget.configure(
            bg=theme["button_bg"], 
            fg=theme["button_fg"]
        )