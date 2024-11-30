#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os


class SuricataAnsibleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Suricata & Ansible Management")

        # Path to the inventory file
        self.inventory_file = "/home/tomas/ansible_projeto1/inventory"

        # Creating the Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # ---------------------- Inventory Tab ----------------------
        self.inventory_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.inventory_frame, text="Inventory")

        self.ip_label = tk.Label(self.inventory_frame, text="IP Address:")
        self.ip_label.grid(row=0, column=0)
        self.ip_entry = tk.Entry(self.inventory_frame)
        self.ip_entry.grid(row=0, column=1)

        self.user_label = tk.Label(self.inventory_frame, text="Username:")
        self.user_label.grid(row=1, column=0)
        self.user_entry = tk.Entry(self.inventory_frame)
        self.user_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self.inventory_frame, text="Password:")
        self.password_label.grid(row=2, column=0)
        self.password_entry = tk.Entry(self.inventory_frame, show="*")
        self.password_entry.grid(row=2, column=1)

        # Buttons for Inventory Management
        self.save_inventory_button = tk.Button(self.inventory_frame, text="New Server", command=self.save_server)
        self.save_inventory_button.grid(row=3, column=0)

        self.load_inventory_button = tk.Button(self.inventory_frame, text="Load Inventory", command=self.load_inventory)
        self.load_inventory_button.grid(row=4, columnspan=2)

        self.inventory_text = tk.Text(self.inventory_frame, height=10, width=50)
        self.inventory_text.grid(row=5, columnspan=2)

        self.delete_button = tk.Button(self.inventory_frame, text="Delete Server", command=self.delete_server)
        self.delete_button.grid(row=6, columnspan=2)

        # ---------------------- Install Suricata Tab ----------------------
        self.install_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.install_frame, text="Install Suricata")

        self.interface_label = tk.Label(self.install_frame, text="Network Interface:")
        self.interface_label.grid(row=0, column=0)
        self.interface_entry = tk.Entry(self.install_frame)
        self.interface_entry.grid(row=0, column=1)

        self.run_playbook_button = tk.Button(self.install_frame, text="Install Suricata", command=self.install_suricata)
        self.run_playbook_button.grid(row=1, columnspan=2)

        # ---------------------- Suricata Logs Tab ----------------------
        self.logs_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.logs_frame, text="Suricata Logs")

        self.view_logs_button = tk.Button(self.logs_frame, text="View Logs", command=self.view_logs)
        self.view_logs_button.grid(row=0, columnspan=2)

        self.log_text = tk.Text(self.logs_frame, height=10, width=50)
        self.log_text.grid(row=1, columnspan=2)

        # ---------------------- Custom Rules Tab ----------------------
        self.rules_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.rules_frame, text="Custom Rules")

        self.action_label = tk.Label(self.rules_frame, text="Action:")
        self.action_label.grid(row=0, column=0)
        self.action_var = tk.StringVar()
        self.action_dropdown = tk.OptionMenu(self.rules_frame, self.action_var, "alert", "pass", "drop", "reject", "log")
        self.action_dropdown.grid(row=0, column=1)

        self.protocol_label = tk.Label(self.rules_frame, text="Protocol:")
        self.protocol_label.grid(row=1, column=0)
        self.protocol_entry = tk.Entry(self.rules_frame)
        self.protocol_entry.grid(row=1, column=1)

        self.src_ip_label = tk.Label(self.rules_frame, text="Source IP:")
        self.src_ip_label.grid(row=2, column=0)
        self.src_ip_entry = tk.Entry(self.rules_frame)
        self.src_ip_entry.grid(row=2, column=1)

        self.src_port_label = tk.Label(self.rules_frame, text="Source Port:")
        self.src_port_label.grid(row=3, column=0)
        self.src_port_entry = tk.Entry(self.rules_frame)
        self.src_port_entry.grid(row=3, column=1)

        self.dst_ip_label = tk.Label(self.rules_frame, text="Destination IP:")
        self.dst_ip_label.grid(row=4, column=0)
        self.dst_ip_entry = tk.Entry(self.rules_frame)
        self.dst_ip_entry.grid(row=4, column=1)

        self.dst_port_label = tk.Label(self.rules_frame, text="Destination Port:")
        self.dst_port_label.grid(row=5, column=0)
        self.dst_port_entry = tk.Entry(self.rules_frame)
        self.dst_port_entry.grid(row=5, column=1)

        self.msg_label = tk.Label(self.rules_frame, text="Message:")
        self.msg_label.grid(row=6, column=0)
        self.msg_entry = tk.Entry(self.rules_frame)
        self.msg_entry.grid(row=6, column=1)

        self.sid_label = tk.Label(self.rules_frame, text="SID:")
        self.sid_label.grid(row=7, column=0)
        self.sid_entry = tk.Entry(self.rules_frame)
        self.sid_entry.grid(row=7, column=1)

        self.add_rule_button = tk.Button(self.rules_frame, text="Add Rule", command=self.add_rule)
        self.add_rule_button.grid(row=8, columnspan=2)

        self.view_custom_rules_button = tk.Button(self.rules_frame, text="View Custom Rules", command=self.view_custom_rules)
        self.view_custom_rules_button.grid(row=9, columnspan=2)

        self.custom_rules_text = tk.Text(self.rules_frame, height=10, width=50)
        self.custom_rules_text.grid(row=10, columnspan=2)

    # ---------------------- Inventory Functions ----------------------
    def load_inventory(self):
        try:
            with open(self.inventory_file, "r") as file:
                content = file.read()
                self.inventory_text.delete(1.0, tk.END)
                self.inventory_text.insert(tk.END, content)
        except FileNotFoundError:
            messagebox.showerror("Error", "Inventory file not found.")

    def save_server(self):
        new_server = f"{self.ip_entry.get()} ansible_user={self.user_entry.get()} ansible_become_password={self.password_entry.get()}\n"
        try:
            with open(self.inventory_file, "a") as file:
                file.write(new_server)
            self.load_inventory()
            messagebox.showinfo("Success", "New server added.")
        except IOError:
            messagebox.showerror("Error", "Failed to write to inventory file.")

   
    def delete_server(self):
        try:
            selected_line = self.inventory_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()
            with open(self.inventory_file, "r+") as file:
                lines = file.readlines()
                file.seek(0)
                for line in lines:
                    if line.strip() != selected_line:
                        file.write(line)
                file.truncate()
            self.load_inventory()
            messagebox.showinfo("Success", "Server deleted.")
        except tk.TclError:
            messagebox.showerror("Error", "Select a server to delete.")
        except IOError:
            messagebox.showerror("Error", "Failed to delete server from inventory file.")

    # ---------------------- Install Suricata ----------------------
    def install_suricata(self):
        playbook_path = os.path.expanduser("~/ansible_projeto1/install_suricata.yml")
        interface = self.interface_entry.get()  # Get the interface input from the user

        # Check if the interface field is not empty
        if not interface:
            messagebox.showerror("Error", "Network interface is required.")
            return

        try:
            # Run the Ansible playbook with the interface as an extra variable
            subprocess.run([
                "ansible-playbook", 
                "-i", self.inventory_file, 
                playbook_path,
                "-e", f"network_interface={interface}"
            ], check=True)
            messagebox.showinfo("Success", f"Suricata installation started on interface: {interface}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to install Suricata: {e}")

    # ---------------------- View Suricata Logs ---------------------
    def view_logs(self):
        log_file = "/var/log/suricata/fast.log"  # Adjust this path if needed
        if not os.path.exists(log_file):
            messagebox.showerror("Error", "Log file not found. Please ensure Suricata is running.")
            return
        try:
            with open(log_file, "r") as file:
                logs = file.read()
                self.log_text.delete(1.0, tk.END)  # Clear the text box
                self.log_text.insert(tk.END, logs)  # Insert the logs
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read log file: {e}")

    # ---------------------- Custom Rules Functions ----------------------
    def add_rule(self):
        action = self.action_var.get()
        protocol = self.protocol_entry.get()
        src_ip = self.src_ip_entry.get()
        src_port = self.src_port_entry.get()
        dst_ip = self.dst_ip_entry.get()
        dst_port = self.dst_port_entry.get()
        msg = self.msg_entry.get()
        sid = self.sid_entry.get()

        # Ensure all fields are filled
        if not all([action, protocol, src_ip, src_port, dst_ip, dst_port, msg, sid]):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        rule = f"{action} {protocol} {src_ip} {src_port} -> {dst_ip} {dst_port} (msg:\"{msg}\"; sid:{sid};)\n"
        custom_rules_path = "/etc/suricata/rules/custom.rules"

        try:
            with open(custom_rules_path, "a") as file:
                file.write(rule)
            self.view_custom_rules()
            messagebox.showinfo("Success", "Custom rule added.")
        except IOError:
            messagebox.showerror("Error", "Failed to add custom rule.")

    def view_custom_rules(self):
        custom_rules_path = "/etc/suricata/rules/custom.rules"
        if not os.path.exists(custom_rules_path):
            messagebox.showerror("Error", "Custom rules file not found.")
            return
        try:
            with open(custom_rules_path, "r") as file:
                custom_rules = file.read()
                self.custom_rules_text.delete(1.0, tk.END)
                self.custom_rules_text.insert(tk.END, custom_rules)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read custom rules file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    gui = SuricataAnsibleGUI(root)
    root.mainloop()
