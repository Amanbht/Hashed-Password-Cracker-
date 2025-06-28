import threading
import time
import customtkinter as ctk
from tkinter import filedialog, messagebox
from attacks import brute_force_crack, dictionary_attack, rainbow_table_crack
from utils import is_possibly_salted, detect_hash_type
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("700x750")
app.title("🔐 Hashed Password Cracker")

hash_file_path = None
start_time = None
after_jobs = []

def schedule_after(delay, callback):
    job_id = app.after(delay, callback)
    after_jobs.append(job_id)
    return job_id

def select_file():
    global hash_file_path
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if path:
        hash_file_path = path
        file_label.configure(text=f"Selected: {path.split('/')[-1]}")

def update_progress(val):
    progress_bar.set(val / 100)
    elapsed = time.time() - start_time
    if val > 0:
        est_total = elapsed / (val / 100)
        remaining = est_total - elapsed
        eta_label.configure(text=f"⏳ ETA: {int(remaining)}s")
    else:
        eta_label.configure(text="⏳ ETA: calculating...")

def crack_single_hash(hash_val, method):
    algo = detect_hash_type(hash_val)
    if algo == "unknown":
        return "❌ Unknown Hash Format"
    if method == "Brute Force":
        return brute_force_crack(hash_val, algo, progress_callback=update_progress)
    elif method == "Dictionary":
        return dictionary_attack(hash_val, algo, progress_callback=update_progress)
    elif method == "Rainbow Table":
        return rainbow_table_crack(hash_val, algo)
    return None

def show_summary_chart_embedded(results: dict):
    def plot():
        try:
            for widget in chart_frame.winfo_children():
                widget.destroy()

            success = sum(1 for res in results.values() if res not in ["Not Found", "Possibly Salted or Uncrackable", "❌ Unknown Hash Format"])
            not_found = sum(1 for res in results.values() if res == "Not Found")
            salted = sum(1 for res in results.values() if "Salted" in res)
            unknown = sum(1 for res in results.values() if "Unknown" in res)

            labels = ['Cracked', 'Not Found', 'Salted', 'Unknown Format']
            sizes = [success, not_found, salted, unknown]
            colors = ['green', 'red', 'orange', 'gray']

            fig, ax = plt.subplots(figsize=(4, 4))
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors)
            ax.set_title("Hash Cracking Results")
            ax.axis('equal')

            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack()
        except Exception as e:
            print("Chart error:", e)

    schedule_after(0, plot)

def crack_worker():
    global start_time
    hash_val = hash_entry.get()
    method = method_dropdown.get()
    start_time = time.time()

    if not method:
        messagebox.showwarning("Missing Info", "Select cracking method.")
        return

    results = {}

    if hash_file_path:
        with open(hash_file_path, "r", encoding="utf-8") as file:
            hashes = [line.strip() for line in file if line.strip()]
        for h in hashes:
            progress_bar.set(0)
            eta_label.configure(text="⏳ ETA: calculating...")
            status_label.configure(text=f"Cracking {h[:10]}...")
            app.update_idletasks()
            result = crack_single_hash(h, method)
            if result:
                results[h] = result
            else:
                if is_possibly_salted(h, result, detect_hash_type(h)):
                    results[h] = "Possibly Salted or Uncrackable"
                else:
                    results[h] = "Not Found"
    else:
        if not hash_val:
            messagebox.showwarning("Missing Hash", "Enter a hash or select file.")
            return
        result = crack_single_hash(hash_val, method)
        if result:
            results[hash_val] = result
        else:
            if is_possibly_salted(hash_val, result, detect_hash_type(hash_val)):
                results[hash_val] = "Possibly Salted or Uncrackable"
            else:
                results[hash_val] = "Not Found"

    # ✅ Save results to file with UTF-8 encoding (fix for Unicode errors)
    with open("cracked_results.txt", "w", encoding="utf-8") as f:
        for h, res in results.items():
            f.write(f"{h} => {res}\n")

    progress_bar.set(0)
    eta_label.configure(text="✅ Done")
    status_label.configure(text="✅ Results saved to cracked_results.txt")

    if any("Salted" in v for v in results.values()):
        messagebox.showwarning("Salt Alert", "Some hashes may be salted and cannot be cracked without salt.")

    show_summary_chart_embedded(results)

def start_cracking():
    threading.Thread(target=crack_worker, daemon=True).start()

def on_closing():
    try:
        print("Closing app safely...")
        for job_id in after_jobs:
            try:
                app.after_cancel(job_id)
            except:
                pass
        app.destroy()
    except Exception:
        pass

# === GUI Layout ===
ctk.CTkLabel(app, text="🔐 Hashed Password Cracker", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=10)

hash_entry = ctk.CTkEntry(app, placeholder_text="Enter single hash (or use file)", width=500)
hash_entry.pack(pady=10)

method_dropdown = ctk.CTkComboBox(app, values=["Brute Force", "Dictionary", "Rainbow Table"], width=200)
method_dropdown.set("Dictionary")
method_dropdown.pack(pady=5)

ctk.CTkButton(app, text="Select Hash File", command=select_file).pack(pady=5)
file_label = ctk.CTkLabel(app, text="No file selected")
file_label.pack()

ctk.CTkButton(app, text="Start Cracking", command=start_cracking).pack(pady=10)

progress_bar = ctk.CTkProgressBar(app, width=400)
progress_bar.pack(pady=10)
progress_bar.set(0)

eta_label = ctk.CTkLabel(app, text="⏳ ETA: --", text_color="lightgray")
eta_label.pack(pady=2)

status_label = ctk.CTkLabel(app, text="Idle", text_color="lightgray")
status_label.pack(pady=5)

ctk.CTkLabel(app, text="📊 Summary Chart Below", font=ctk.CTkFont(size=14)).pack(pady=5)
chart_frame = ctk.CTkFrame(app, width=500, height=300)
chart_frame.pack(pady=5)

ctk.CTkButton(app, text="Exit", command=on_closing).pack(pady=10)

ctk.CTkLabel(app, text="© 2025 Aman | GPT-built", font=ctk.CTkFont(size=10)).pack(side="bottom", pady=5)

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()
