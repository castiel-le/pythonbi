# How to Run This Python Project

This guide shows you how to set up and run this project step by step.

---

## What You Need
- Windows computer  
- Internet connection  
- Python  
- Visual Studio Code (VSCode)

---

## Step 1: Install Python and VSCode

1. Download and install **Python (latest 64-bit Windows version)** from:  
   https://www.python.org/downloads/

   ⚠️ During installation, make sure to tick **“Add Python to PATH”**.

2. Download and install **Visual Studio Code (VSCode)** from:  
   https://code.visualstudio.com/

---

## Step 2: Open the Project Folder in VSCode

1. Open **VSCode**
2. Click **File → Open Folder**
3. Select the project folder
4. Click **Open**

---

## Step 3: Upgrade pip (in VSCode Terminal)

1. In VSCode, open the terminal:
   - Click **Terminal → New Terminal**

2. Run this command:
```
python -m pip install --upgrade pip
```
---

## Step 4: Install required libraries

In the same terminal, run:
```
pip install -r requirements.txt
```
(This installs all the libraries the program needs.)

---

## Step 5: Run the program

Run the Python file using:
```
python filename.py
```
Replace `filename.py` with the actual file name.

Example:
```
python main.py
```
---

## Done 🎉
If there are no error messages, the program is running correctly.