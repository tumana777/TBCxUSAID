import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

conversion_rates = {
    ("USD", "GEL"): 2.69,
    ("EUR", "GEL"): 2.97,
    ("TRY", "GEL"): 0.08,
    ("CNY", "GEL"): 0.38,
    ("GEL", "USD"): 1/2.69,
    ("GEL", "EUR"): 1/2.97,
    ("GEL", "TRY"): 1/0.08,
    ("GEL", "CNY"): 1/0.38,
    ("USD", "EUR"): 2.69/2.97,
    ("USD", "TRY"): 2.69/0.08,
    ("USD", "CNY"): 2.69/0.38,
    ("EUR", "USD"): 2.97/2.69,
    ("EUR", "TRY"): 2.97/0.08,
    ("EUR", "CNY"): 2.97/0.38,
    ("TRY", "USD"): 0.08/2.69,
    ("TRY", "EUR"): 0.08/2.97,
    ("TRY", "CNY"): 0.08/0.38,
    ("CNY", "USD"): 0.38/2.69,
    ("CNY", "EUR"): 0.38/2.97,
    ("CNY", "TRY"): 0.38/0.08,
}

currencies = ["USD", "EUR", "TRY", "CNY", "GEL"]

def update_to_currency(*args):
    from_currency = from_currency_var.get()
    filtered_currencies = [currency for currency in currencies if currency != from_currency]
    to_currency_combobox.config(values=filtered_currencies)
    if to_currency_var.get() == from_currency:
        to_currency_var.set(filtered_currencies[0])

def convert():
    amount_str = amount_entry.get()
    if not amount_str:
        messagebox.showwarning("Input Error", "Please enter an amount to convert.")
        return
    
    amount = float(amount_str)
    from_currency = from_currency_var.get()
    to_currency = to_currency_var.get()
    result = amount * conversion_rates[(from_currency, to_currency)]
    result_var.set(f"{result:.2f} {to_currency}")

def clear():
    amount_entry.delete(0, tk.END)
    result_var.set("")
    from_currency_var.set("USD")
    to_currency_var.set("GEL")

def validate_input(input):
    if len(input) > 10:
        return False
    if input == "" or input.replace(".", "", 1).isdigit():
        return True
    else:
        return False

root = tk.Tk()
root.title("Currency Converter")

x_position = int(root.winfo_screenwidth() / 2 - 150)
y_position = 100

root.geometry(f"300x300+{x_position}+{y_position}")
root.resizable(False, False)

style = ttk.Style()
style.map('TCombobox', fieldbackground=[('readonly', 'white')],
          selectbackground=[('readonly', 'white')],
          selectforeground=[('readonly', 'black')])

validate_float = root.register(validate_input)

amount_label = tk.Label(root, text="Amount:")
amount_label.grid(row=0, column=0, padx=10, pady=10)

amount_entry = tk.Entry(root, validate="key", validatecommand=(validate_float, "%P"))
amount_entry.grid(row=0, column=1, padx=10, pady=10)

from_currency_var = tk.StringVar(value="USD")
from_currency_var.trace("w", update_to_currency)

from_currency_label = tk.Label(root, text="From:")
from_currency_label.grid(row=1, column=0, padx=10, pady=10)

from_currency_combobox = ttk.Combobox(root, textvariable=from_currency_var, values=currencies, state="readonly", style='TCombobox')
from_currency_combobox.grid(row=1, column=1, padx=10, pady=10)

to_currency_var = tk.StringVar(value="GEL")
to_currency_label = tk.Label(root, text="To:")
to_currency_label.grid(row=2, column=0, padx=10, pady=10)

to_currency_combobox = ttk.Combobox(root, textvariable=to_currency_var, values=[currency for currency in currencies if currency != from_currency_var.get()], state="readonly", style='TCombobox')
to_currency_combobox.grid(row=2, column=1, padx=10, pady=10)

convert_button = tk.Button(root, text="Convert", command=convert)
convert_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

result_var = tk.StringVar()
result_label = tk.Label(root, textvariable=result_var)
result_label.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

clear_button = tk.Button(root, text="Clear", command=clear)
clear_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

root.mainloop()
