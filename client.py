import tkinter as tk
from tkinter import ttk

def on_button_click():
    label.config(text="Button clicked!")

# Create the main window
root = tk.Tk()
root.title("Basic Tkinter App")
root.geometry("300x200")  # width x height

# Create a label
label = ttk.Label(root, text="Hello, Tkinter!")
label.pack(pady=10)

# Create a button
button = ttk.Button(root, text="Click Me", command=on_button_click)
button.pack(pady=10)

# Run the application
root.mainloop()
