#!/usr/bin/env python3
import tkinter as tk
import subprocess
import os

# Create the main window
root = tk.Tk()
root.title("Suricata GUI")

# Set the window size to 300x200 pixels
root.geometry("300x200")

# Define functions for each button
def install_suricata():
    # Define the path to the playbook and inventory
    playbook_path = os.path.expanduser("~/ansible_projeto1/install_suricata.yml")
    inventory_path = os.path.expanduser("~/ansible_projeto1/inventory")

    # Run the shell command using subprocess
    try:
        subprocess.run(["ansible-playbook", "-i", inventory_path, playbook_path], check=True)
        print("Suricata installation started.")
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")

# Create buttons
install_button = tk.Button(root, text="Install Suricata", command=install_suricata)

# Place buttons in the window
install_button.pack(pady=10)

# Run the application
root.mainloop()

