import tkinter as tk
from tkinter import ttk
import psutil
import threading
import time
from collections import Counter

def update_stats():
    while True:
        # CPU and Memory usage
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent

        cpu_label.config(text=f"CPU Usage: {cpu_percent}%")
        cpu_progress['value'] = cpu_percent

        memory_label.config(text=f"Memory Usage: {memory_percent}%")
        memory_progress['value'] = memory_percent

        # High resource usage warning
        if cpu_percent > 80 or memory_percent > 80:
            warning_label.config(text="⚠️ High Resource Usage Detected!")
        else:
            warning_label.config(text="")

        # Top 5 CPU consuming processes
        processes = sorted(psutil.process_iter(['pid', 'name', 'cpu_percent']),
                           key=lambda p: p.info['cpu_percent'], reverse=True)[:5]

        process_text = "Top 5 Processes (by CPU):\n"
        for proc in processes:
            try:
                process_text += f"{proc.info['name']} (PID: {proc.info['pid']}) - {proc.info['cpu_percent']}%\n"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        process_label.config(text=process_text)

        # Process state summary
        statuses = Counter()
        for p in psutil.process_iter(['status']):
            try:
                statuses[p.info['status']] += 1
            except:
                continue

        status_text = "Process States:\n"
        for state, count in statuses.items():
            status_text += f"{state}: {count}\n"
        status_label.config(text=status_text)

        time.sleep(2)

def kill_process():
    try:
        pid = int(pid_entry.get())
        p = psutil.Process(pid)
        p.terminate()
        result_label.config(text=f"✅ Terminated PID {pid}")
    except Exception as e:
        result_label.config(text=f"❌ Error: {e}")

# -------------------- GUI Setup --------------------
root = tk.Tk()
root.title("System Monitor Dashboard")
root.geometry("400x600")

# CPU usage
cpu_label = tk.Label(root, text="CPU Usage:", font=("Arial", 14))
cpu_label.pack(pady=5)

cpu_progress = ttk.Progressbar(root, length=300, mode='determinate')
cpu_progress.pack(pady=5)

# Memory usage
memory_label = tk.Label(root, text="Memory Usage:", font=("Arial", 14))
memory_label.pack(pady=5)

memory_progress = ttk.Progressbar(root, length=300, mode='determinate')
memory_progress.pack(pady=5)

# High resource usage warning
warning_label = tk.Label(root, text="", fg="red", font=("Arial", 12))
warning_label.pack(pady=5)

# Top processes
process_label = tk.Label(root, text="", font=("Arial", 10), justify=tk.LEFT)
process_label.pack(pady=5)

# Process state summary
status_label = tk.Label(root, text="", font=("Arial", 10), justify=tk.LEFT)
status_label.pack(pady=5)

# Kill process section
tk.Label(root, text="Enter PID to Terminate:", font=("Arial", 12)).pack(pady=5)
pid_entry = tk.Entry(root)
pid_entry.pack(pady=5)

kill_btn = tk.Button(root, text="Kill Process", command=kill_process)
kill_btn.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 10))
result_label.pack(pady=5)

# Start stats update in a thread
threading.Thread(target=update_stats, daemon=True).start()

root.mainloop()
