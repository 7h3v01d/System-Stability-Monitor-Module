import tkinter as tk
from tkinter import ttk
from monitor import monitor

def update_ui():
    data = monitor.get_stats()
    
    # Update text
    cpu_label.config(text=f"CPU: {data['cpu']}%")
    gpu_label.config(text=f"GPU: {data['gpu']}%")
    
    # Change color if Peak Alert is active
    if data["peak_alert"]:
        status_label.config(text="⚠️ PEAK ALERT: THROTTLING", foreground="red")
    else:
        status_label.config(text="Status: Normal", foreground="green")
    
    root.after(500, update_ui)

root = tk.Tk()
root.title("System Pulse")
root.geometry("250x150")

cpu_label = ttk.Label(root, font=("Arial", 12))
cpu_label.pack(pady=5)

gpu_label = ttk.Label(root, font=("Arial", 12))
gpu_label.pack(pady=5)

status_label = ttk.Label(root, font=("Arial", 10, "bold"))
status_label.pack(pady=10)

update_ui()
root.mainloop()