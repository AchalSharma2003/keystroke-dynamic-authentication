import tkinter as tk
from tkinter import messagebox, ttk
import joblib, os, re
import numpy as np
from time import time
from pynput import keyboard
from sklearn.ensemble import RandomForestClassifier

# === Configuration ===
password_samples = 5
model_dir = "models"
os.makedirs(model_dir, exist_ok=True)

# === Keystroke Capture ===
def collect_keystrokes(password, samples=1):
    data = []
    for i in range(samples):
        press_times, release_times = {}, {}

        def on_press(key):
            try:
                if hasattr(key, 'char') and key.char:
                    press_times[key.char] = time()
            except: pass

        def on_release(key):
            try:
                if hasattr(key, 'char') and key.char:
                    release_times[key.char] = time()
                    if len(release_times) >= len(password):
                        return False
            except: pass

        if samples > 1:
            messagebox.showinfo("Typing Sample", f"Sample {i + 1}: Type the password '{password}'")

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

        if all(c in press_times and c in release_times for c in password):
            dwell = [release_times[c] - press_times[c] for c in password]
            flight = [press_times[password[i]] - release_times[password[i - 1]] for i in range(1, len(password))]
            data.append(dwell + flight)
        else:
            messagebox.showerror("Error", " Incomplete typing. Please try again.")
            return None
    return data

# === Model Training ===
def train_model(username, password, data):
    safe_username = re.sub(r'\W+', '_', username.strip())
    safe_password = re.sub(r'\W+', '_', password.strip())

    os.makedirs(model_dir, exist_ok=True)
    filename = os.path.join(os.path.dirname(__file__), model_dir, f"{safe_username}_{safe_password}_model.pkl")

    impostors = np.array(data) + np.random.normal(0, 0.03, size=(len(data), len(data[0])))
    model_data = data + impostors.tolist()
    labels = [1] * len(data) + [0] * len(impostors)

    model = RandomForestClassifier()
    model.fit(model_data, labels)

    joblib.dump(model, filename)
    print(" Model saved to:", filename)
    return filename

# === Authentication ===
def authenticate(username, password):
    safe_username = re.sub(r'\W+', '_', username.strip())
    safe_password = re.sub(r'\W+', '_', password.strip())
    filename = os.path.join(os.path.dirname(__file__), model_dir, f"{safe_username}_{safe_password}_model.pkl")

    if not os.path.exists(filename):
        messagebox.showerror("Login Failed", " Model not found. Please register first.")
        return

    model = joblib.load(filename)
    sample = collect_keystrokes(password, samples=1)
    if not sample:
        return

    prob = model.predict_proba([sample[0]])[0][1]
    if prob >= 0.5:
        messagebox.showinfo("Login Success", " Access Granted!")
    else:
        messagebox.showerror("Login Failed", " Access Denied. Typing pattern doesn't match.")

# === GUI Setup ===
app = tk.Tk()
app.title("Keystroke Authentication System")

notebook = ttk.Notebook(app)
login_tab = ttk.Frame(notebook)
register_tab = ttk.Frame(notebook)
notebook.add(login_tab, text="Login")
notebook.add(register_tab, text="Register")
notebook.pack(expand=1, fill="both")

# === Login Tab ===
tk.Label(login_tab, text="Username").pack(pady=5)
login_user = tk.Entry(login_tab)
login_user.pack()

tk.Label(login_tab, text="Password").pack(pady=5)
login_pass = tk.Entry(login_tab, show="*")
login_pass.pack()

tk.Button(login_tab, text="Login", command=lambda: authenticate(
    login_user.get().strip(), login_pass.get().strip())).pack(pady=15)

# === Register Tab ===
tk.Label(register_tab, text="New Username").pack(pady=5)
reg_user = tk.Entry(register_tab)
reg_user.pack()

tk.Label(register_tab, text="Password to Register With").pack(pady=5)
reg_pass = tk.Entry(register_tab)  # Optional: remove show="*" for visibility
reg_pass.pack()

def handle_registration():
    username = reg_user.get().strip()
    password = reg_pass.get().strip()
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password.")
        return

    data = collect_keystrokes(password, samples=password_samples)
    if data:
        model_path = train_model(username, password, data)
        messagebox.showinfo("Registration Complete", f" Model trained and saved:\n{model_path}")

tk.Button(register_tab, text="Register", command=handle_registration).pack(pady=15)

# === Run App ===
app.geometry("550x380")
app.mainloop()
