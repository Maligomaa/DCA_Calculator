import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def exp_decline (Qi,Di,t):
    return Qi * np.exp(-Di * t)

def hyp_decline (t, Qi, Di, b):
    return Qi / ((1 + b * Di * t) ** (1 / b))

def harm_decline (t, Qi, Di):
    return Qi / (1 + Di * t)

def calculate():

    try:
        Qi = float(entry_Qi.get())
        Di = float(entry_Di.get())
        b = float(entry_b.get())
        t = float(entry_t.get())
        
        
        t = np.arange(0, t+1, 1)

        if b == 0:
            q = exp_decline (Qi,Di,t)
            cum=q*365
            dtype= "Exponential"

        elif 0<b<1:
            q = hyp_decline (t, Qi, Di, b)
            cum=q*365
            dtype= "Hyperbolic"
    
        elif b == 1:
            q = harm_decline (t, Qi, Di)
            cum=q*365
            dtype= "Harmonic"
        else:
            messagebox.showerror("Input Error", "Exponent b must be 0 (exp), 1 (harm), or between 0 and 1 (hyp).")
            return
        
        cumprod = np.trapezoid(cum, t)

        ax.clear()
        ax.plot(t, q, marker="o", label="Production Profile", color="blue")
        ax.set_title(f"Calculated Production Profile ({dtype})")
        ax.set_xlabel("Time (years)")
        ax.set_ylabel("Production Rate (m³/day)")
        ax.grid(True)
        ax.legend()
        canvas.draw()
      
        cum_label.config(text=f"Cum.Prod.= {int(cumprod)} m³")
        for row in tree.get_children():
            tree.delete(row)
        for i in range(len(t)):
            tree.insert("", "end", values=(f"{t[i]:.0f}", f"{q[i]:.2f}"))
         

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")
        

root = tk.Tk()
root.title("DCA Production Profile Calculator")
root.geometry("800x700")
root.resizable(False, False)

tk.Label(root, text="").grid(row=0, column=0, padx=10, pady=2, sticky="e")

tk.Label(root, text="Initial Production Rate (Qi)").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_Qi = tk.Entry(root, width=10)
entry_Qi.grid(row=1, column=1, padx=10, pady=5)
tk.Label(root, text="[m3/d]").grid(row=1, column=2, padx=10, pady=5, sticky="w")

tk.Label(root, text="Annual Decline Rate (Di)").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_Di = tk.Entry(root, width=10)
entry_Di.grid(row=2, column=1, padx=10, pady=5)
tk.Label(root, text="[1/year]").grid(row=2, column=2, padx=10, pady=5, sticky="w")

tk.Label(root, text="Exponent (b)").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_b = tk.Entry(root, width=10)
entry_b.grid(row=3, column=1, padx=10, pady=5)
tk.Label(root, text="0(exp), 1(harm), 0<b<1(hyp)").grid(row=3, column=2, padx=10, pady=5, sticky="w")

tk.Label(root, text="Time Span (t)").grid(row=4, column=0, padx=10, pady=5, sticky="e")
entry_t = tk.Entry(root, width=10)
entry_t.grid(row=4, column=1, padx=10, pady=5)
tk.Label(root, text="[years]").grid(row=4, column=2, padx=10, pady=5, sticky="w")

cum_label = tk.Label(root, text="------ m³", font=("Arial", 12, "bold"))
cum_label.grid(row=5, column=2, padx=10, pady=5, sticky="e")

tk.Button(root, width=16, text="Calculate", font=("Arial", 12, "bold"),command=calculate).grid(row=5, column=0, columnspan=2, pady=5)

fig, ax = plt.subplots(figsize=(5, 4.5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=6, column=0, columnspan=2, pady=10)

tree = ttk.Treeview(root, columns=("Time", "Rate"), show="headings", height=21)
tree.heading("Time", text="Year")
tree.heading("Rate", text="Production Rate (m³/day)")
tree.column("Time", width=80, anchor="center")
tree.column("Rate", width=200, anchor="center")
tree.grid(row=6, column=2, columnspan=2, padx=10, pady=10)

root.mainloop()




