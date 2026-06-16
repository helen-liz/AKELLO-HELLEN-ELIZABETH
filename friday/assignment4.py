import tkinter as tk
from tkinter import messagebox

# Operation functions

def get_inputs():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        return a, b
    except ValueError:
        messagebox.showerror("Input error", "Please enter valid numbers.")
        return None


def add():
    vals = get_inputs()
    if vals:
        a, b = vals
        result_var.set(str(a + b))


def subtract():
    vals = get_inputs()
    if vals:
        a, b = vals
        result_var.set(str(a - b))


def multiply():
    vals = get_inputs()
    if vals:
        a, b = vals
        result_var.set(str(a * b))


def divide():
    vals = get_inputs()
    if vals:
        a, b = vals
        if b == 0:
            messagebox.showerror("Math error", "Cannot divide by zero.")
            return
        result_var.set(str(a / b))


def clear():
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    result_var.set("")


# Build UI
root = tk.Tk()
root.title("Menu-driven Calculator")
root.resizable(False, False)

frame = tk.Frame(root, padx=12, pady=12)
frame.pack()

label_a = tk.Label(frame, text="Number A:")
label_a.grid(row=0, column=0, sticky="e")
entry_a = tk.Entry(frame, width=20)
entry_a.grid(row=0, column=1, pady=4)

label_b = tk.Label(frame, text="Number B:")
label_b.grid(row=1, column=0, sticky="e")
entry_b = tk.Entry(frame, width=20)
entry_b.grid(row=1, column=1, pady=4)

result_var = tk.StringVar()
result_label = tk.Label(frame, textvariable=result_var, width=24, anchor="w", relief="sunken")
result_label.grid(row=2, column=0, columnspan=2, pady=(8, 4))

# Buttons for quick access
btn_frame = tk.Frame(frame)
btn_frame.grid(row=3, column=0, columnspan=2, pady=(6,0))

btn_add = tk.Button(btn_frame, text="Add", width=10, command=add)
btn_add.grid(row=0, column=0, padx=4)
btn_sub = tk.Button(btn_frame, text="Subtract", width=10, command=subtract)
btn_sub.grid(row=0, column=1, padx=4)
btn_mul = tk.Button(btn_frame, text="Multiply", width=10, command=multiply)
btn_mul.grid(row=0, column=2, padx=4)
btn_div = tk.Button(btn_frame, text="Divide", width=10, command=divide)
btn_div.grid(row=0, column=3, padx=4)
btn_clear = tk.Button(btn_frame, text="Clear", width=10, command=clear)
btn_clear.grid(row=0, column=4, padx=4)

# Menu (menu-driven)
menubar = tk.Menu(root)
ops_menu = tk.Menu(menubar, tearoff=0)
ops_menu.add_command(label="Add", command=add)
ops_menu.add_command(label="Subtract", command=subtract)
ops_menu.add_command(label="Multiply", command=multiply)
ops_menu.add_command(label="Divide", command=divide)
ops_menu.add_separator()
ops_menu.add_command(label="Clear", command=clear)
ops_menu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="Operations", menu=ops_menu)

help_menu = tk.Menu(menubar, tearoff=0)
help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "Menu-driven GUI calculator.\nUses functions for operations."))
menubar.add_cascade(label="Help", menu=help_menu)

root.config(menu=menubar)

if __name__ == '__main__':
    root.mainloop()
