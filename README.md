# ⌨️ Keystroke Dynamics Authentication System

A behavioral biometric authentication system that verifies users based on **how they type a password**, not just **what they type**. This project enhances traditional password-based security by analyzing keystroke timing patterns using machine learning.

---

## 📌 Project Description

Keystroke Dynamics Authentication is a **behavior-based security system** that captures a user's typing rhythm and uses it as an additional layer of authentication. Even if an attacker knows the password, access is denied if the typing pattern does not match the legitimate user.

The system records keystroke timings during registration, trains a machine learning model, and verifies the user during login using the same behavioral features.

---

## ✨ Key Features

- 🔐 Behavioral biometric authentication
- ⌨️ Dwell time and flight time analysis
- 🧠 Machine learning using Random Forest Classifier
- 🖥️ User-friendly GUI with Tkinter
- 📁 Individual trained model per user
- 🚫 Protection against password theft attacks

---

## 🛠️ Technologies Used

- Python
- Tkinter (GUI)
- Scikit-learn
- NumPy
- Joblib
- Pynput

---


---

## ⚙️ System Working

### 1️⃣ Registration Phase
- User enters username and password
- User types the password multiple times
- The system captures:
  - **Dwell Time** (Key press to key release)
  - **Flight Time** (Time between consecutive keystrokes)
- A Random Forest classifier is trained
- The trained model is saved locally

---

### 2️⃣ Authentication Phase
- User enters credentials
- Types the password once
- Keystroke features are extracted
- Machine learning model predicts authentication probability
- Access is granted or denied based on the result

---









