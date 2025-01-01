import tkinter as tk
from tkinter import Scrollbar, Listbox

# Global variables
last_result = None
is_new_input = True  # Tracks if the next input should clear the entry


def evaluate(event=None):
    global last_result, is_new_input
    try:
        result = eval(entry.get())
        result = round(result, 10)  # Format to avoid floating-point issues
        add_to_history(f"{entry.get()} = {result}")
        entry.delete(0, tk.END)
        entry.insert(tk.END, str(result))
        last_result = result
        is_new_input = True
    except Exception:
        entry.delete(0, tk.END)
        entry.insert(tk.END, "Error")
        last_result = None
        is_new_input = True


def add_to_expression(value):
    global last_result, is_new_input
    current_text = entry.get()

    if current_text == "Error":  # Clear 'Error' message for any input
        entry.delete(0, tk.END)

    if is_new_input:
        if value.isdigit() or value == ".":  # Clear only for numeric inputs
            entry.delete(0, tk.END)
            is_new_input = False

    entry.insert(tk.END, value)  # Append the input


def handle_keypress(event):
    global is_new_input
    current_text = entry.get()

    if current_text == "Error" and (event.char.isdigit() or event.char == "."):  # Clear 'Error' for valid inputs
        entry.delete(0, tk.END)

    if is_new_input:
        if event.char.isdigit() or event.char == ".":  # Clear on number input
            entry.delete(0, tk.END)
            is_new_input = False
        elif event.char in "+-*/":  # Allow operators after the answer
            is_new_input = False


def clear():
    global last_result, is_new_input
    last_result = None
    is_new_input = True
    entry.delete(0, tk.END)


def add_to_history(calculation):
    history_list.insert(0, calculation)  # Add latest calculation at the top


# Main application window
root = tk.Tk()
root.title("Calculator")
root.geometry("500x600")
root.configure(bg="#2D2D30")

# Display for calculator
entry = tk.Entry(root, font=("Arial", 22), justify="right", bg="#F5F5F5", fg="#2D2D30", borderwidth=2, relief="groove")
entry.pack(fill=tk.BOTH, padx=10, pady=10)

# Bind key events for clearing and evaluating
entry.bind("<Return>", evaluate)  # Evaluate on Enter
entry.bind("<Key>", handle_keypress)  # Handle any keypress
entry.bind("<BackSpace>", lambda event: entry.delete(len(entry.get()) - 1, tk.END))  # Handle backspace

# History Section
history_label = tk.Label(root, text="History", bg="#2D2D30", fg="#FFFFFF", font=("Arial", 14, "bold"))
history_label.pack(pady=(0, 5))

history_frame = tk.Frame(root, bg="#2D2D30", relief="sunken", borderwidth=2)
history_frame.pack(fill=tk.BOTH, padx=10, pady=(0, 10), expand=True)

scrollbar = Scrollbar(history_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

history_list = Listbox(history_frame, yscrollcommand=scrollbar.set, bg="#1E1E1E", fg="#FFFFFF", font=("Arial", 12), selectbackground="#007ACC", selectforeground="#FFFFFF")
history_list.pack(fill=tk.BOTH, expand=True)
scrollbar.config(command=history_list.yview)

# Buttons Section
button_frame = tk.Frame(root, bg="#2D2D30")
button_frame.pack()

# Button styles
button_style = {
    "font": ("Arial", 16),
    "height": 2,
    "width": 5,
    "relief": "raised",
    "borderwidth": 2,
}

# Layout for buttons
buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("C", 4, 0), ("0", 4, 1), ("=", 4, 2), ("+", 4, 3),
]

for (text, row, col) in buttons:
    if text == "=":
        button = tk.Button(button_frame, text=text, command=evaluate, bg="#007ACC", fg="#FFFFFF", **button_style)
    elif text == "C":
        button = tk.Button(button_frame, text=text, command=clear, bg="#E81123", fg="#FFFFFF", **button_style)
    else:
        button = tk.Button(button_frame, text=text, command=lambda t=text: add_to_expression(t), bg="#3A3A3D", fg="#FFFFFF", **button_style)
    button.grid(row=row, column=col, padx=5, pady=5)

# Start the application
root.mainloop()
