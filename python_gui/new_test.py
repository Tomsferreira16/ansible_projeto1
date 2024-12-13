#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os
import json
import base64



class SuricataAnsibleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Suricata & Ansible Management")

        # Path to the inventory file
        self.inventory_file = "/home/tomas/ansible_projeto1/inventory"

        # Creating the Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # ---------------------- Setup Tab ----------------------
        self.setup_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.setup_frame, text="Setup")

        self.key_name_label = tk.Label(self.setup_frame, text="SSH Key Name:")
        self.key_name_label.grid(row=0, column=0)
        self.key_name_entry = tk.Entry(self.setup_frame)
        self.key_name_entry.grid(row=0, column=1)

        self.comment_label = tk.Label(self.setup_frame, text="SSH Key Comment:")
        self.comment_label.grid(row=1, column=0)
        self.comment_entry = tk.Entry(self.setup_frame)
        self.comment_entry.grid(row=1, column=1)

        self.setup_ip_label = tk.Label(self.setup_frame, text="Server IPs (comma separated):")
        self.setup_ip_label.grid(row=2, column=0)
        self.setup_ip_entry = tk.Entry(self.setup_frame)
        self.setup_ip_entry.grid(row=2, column=1)

        self.create_key_button = tk.Button(self.setup_frame, text="Create & Copy SSH Key", command=self.create_and_copy_key)
        self.create_key_button.grid(row=3, columnspan=2)

        # ---------------------- Inventory Tab ----------------------
        self.inventory_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.inventory_frame, text="Inventory")

        self.inventory_ip_label = tk.Label(self.inventory_frame, text="IP Address:")
        self.inventory_ip_label.grid(row=0, column=0)
        self.inventory_ip_entry = tk.Entry(self.inventory_frame)
        self.inventory_ip_entry.grid(row=0, column=1)

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


    # ---------------------- Setup SSH Key Tab ----------------------
    def create_and_copy_key(self):
        key_name = self.key_name_entry.get()
        comment = self.comment_entry.get()
        ips = self.setup_ip_entry.get()

        # Debugging print to check the raw inputs
        print(f"Key Name: '{key_name}', Comment: '{comment}', IPs: '{ips}'")

        if not key_name or not comment or not ips:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        ips = ips.split(",")  # Split the IPs by comma

        try:
            # Get the expanded home directory path
            ssh_dir = os.path.expanduser("~/.ssh/")

            # Check if the SSH key already exists
            key_exists = os.path.isfile(f"{ssh_dir}{key_name}")  # Check if private key exists

            if key_exists:
                # If the key exists, use it directly
                messagebox.showinfo("Info", f"Using existing SSH key: {key_name}")
            else:
                # If the key does not exist, generate a new one
                subprocess.run([
                    "ssh-keygen", "-t", "ed25519", "-f", f"{ssh_dir}{key_name}", "-C", comment, "-N", ""
                ], check=True)
                messagebox.showinfo("Info", f"Created new SSH key: {key_name}")

            # Step 2: Copy the public key to the remote servers
            for ip in ips:
                ip = ip.strip()  # Clean up the IP
                subprocess.run(["ssh-copy-id", "-i", f"{ssh_dir}{key_name}.pub", ip], check=True)

            # Step 3: Add the private key to the SSH agent
            subprocess.run(["eval", "$(ssh-agent -s)"], check=True, shell=True)  # Start the SSH agent
            subprocess.run(["ssh-add", f"{ssh_dir}{key_name}"], check=True)  # Add the private key to the agent

            # Step 4: Create an alias for the ssh-agent setup and add it to .bashrc for persistence
            alias_command = "alias ssha='eval $(ssh-agent) && ssh-add'"
            with open(os.path.expanduser("~/.bashrc"), "a") as bashrc_file:
                bashrc_file.write(f"\n{alias_command}\n")

            # Inform the user of success
            messagebox.showinfo("Success", "SSH Key copied to servers and SSH agent configured.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        except IOError as e:
            messagebox.showerror("Error", f"An error occurred when writing to .bashrc: {e}")


    # ---------------------- Inventory Functions ----------------------
    def save_server(self):
        # Get the input values
        ip = self.inventory_ip_entry.get()
        user = self.user_entry.get()
        password = self.password_entry.get()

        # Check if any of the fields are empty
        if not ip or not user or not password:
            messagebox.showerror("Error", "All fields must be filled.")
            return  # Exit the function if fields are empty

        new_server = f"{ip} ansible_user={user} ansible_become_password={password}\n"
        
        try:
            # Attempt to write to the inventory file
            with open(self.inventory_file, "a") as file:
                file.write(new_server)
            
            # Reload the inventory and show a success message
            self.load_inventory()
            messagebox.showinfo("Success", f"Server {ip} added to inventory.")
        except IOError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def load_inventory(self):
        try:
            # Read the inventory file and display its contents in the text widget
            with open(self.inventory_file, "r") as file:
                inventory = file.read()

            self.inventory_text.delete(1.0, tk.END)  # Clear the current content
            self.inventory_text.insert(tk.END, inventory)  # Insert the new content
        except IOError as e:
            messagebox.showerror("Error", f"An error occurred while reading the inventory file: {e}")


    def delete_server(self):
        try:
            # Get the IP address to delete
            ip = self.inventory_ip_entry.get()

            if not ip:
                messagebox.showerror("Error", "Please enter an IP address to delete.")
                return

            # Read the inventory file and remove the line containing the IP address
            with open(self.inventory_file, "r") as file:
                lines = file.readlines()

            with open(self.inventory_file, "w") as file:
                for line in lines:
                    if ip not in line:
                        file.write(line)

            # Reload the inventory and show a success message
            self.load_inventory()
            messagebox.showinfo("Success", f"Server {ip} deleted from inventory.")
        except IOError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    # ---------------------- Install Suricata ----------------------
    def install_suricata(self):
        interface = self.interface_entry.get()

        if not interface:
            messagebox.showerror("Error", "Please provide a network interface.")
            return

        try:
            # Run the Ansible playbook to install Suricata
            subprocess.run([
                "ansible-playbook", "-i", self.inventory_file, "install_suricata.yml", "--extra-vars", f"interface={interface}"
            ], check=True)

            messagebox.showinfo("Success", "Suricata installation initiated.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while running the playbook: {e}")


    # ---------------------- Suricata Logs ----------------------
    def view_logs(self):
        # Path to your playbook
        playbook_path = "/home/tomas/ansible_projeto1/read_log.yml"  # Update this path if necessary

        try:
            # Run the Ansible playbook and capture the output
            result = subprocess.run(
                [
                    "ansible-playbook", 
                    "-i", self.inventory_file, 
                    playbook_path, 
                    "--extra-vars", "log_path=/var/log/suricata/fast.log"
                ],
                capture_output=True,
                text=True,
                check=True
            )

            # The output of the playbook (stdout)
            playbook_output = result.stdout

            # Check if the playbook output contains the logs or an error message
            if "Error: fast.log file not found." in playbook_output:
                messagebox.showerror("Error", "Suricata fast.log file not found.")
            else:
                # Display the content of fast.log in the text widget
                self.log_text.delete(1.0, tk.END)  # Clear the text box
                self.log_text.insert(tk.END, playbook_output)  # Insert the playbook output

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Ansible playbook execution failed: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view Suricata logs: {e}")




    # ---------------------- Custom Rules ----------------------
    def add_rule(self):
        action = self.action_var.get()
        protocol = self.protocol_entry.get()
        src_ip = self.src_ip_entry.get()
        src_port = self.src_port_entry.get()
        dst_ip = self.dst_ip_entry.get()
        dst_port = self.dst_port_entry.get()
        msg = self.msg_entry.get()
        sid = self.sid_entry.get()

        if not action or not protocol or not src_ip or not src_port or not dst_ip or not dst_port or not msg or not sid:
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        # Format the rule as a string
        rule = f"{action} {protocol} {src_ip} {src_port} -> {dst_ip} {dst_port} (msg:\"{msg}\"; sid:{sid};)"

        # Run Ansible playbook to add the rule
        try:
            subprocess.run([
                "ansible-playbook", "-i", self.inventory_file, "add_custom_rule.yml", 
                "--extra-vars", f"action={action} protocol={protocol} src_ip={src_ip} src_port={src_port} "
                                f"dst_ip={dst_ip} dst_port={dst_port} msg={msg} sid={sid} custom_rule='{rule}'"
            ], check=True)

            # Display success message
            messagebox.showinfo("Success", "Custom rule added.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")


    def view_custom_rules(self):
        try:
            # Run Ansible playbook to fetch custom rules
            result = subprocess.run([
                "ansible-playbook", "-i", self.inventory_file, "view_custom_rules.yml"
            ], capture_output=True, text=True, check=True)

            # Process the output
            if "custom_rules.content" in result.stdout:
                custom_rules = result.stdout.split("custom_rules.content:")[-1].strip()
                custom_rules_decoded = json.loads(custom_rules)['content']
                decoded_rules = base64.b64decode(custom_rules_decoded).decode('utf-8')
                self.custom_rules_text.delete(1.0, tk.END)
                self.custom_rules_text.insert(tk.END, decoded_rules)
            else:
                messagebox.showerror("Error", "Failed to retrieve custom rules.")
        
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")





# ---------------------- Main Program ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SuricataAnsibleGUI(root)
    root.mainloop()