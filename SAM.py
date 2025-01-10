#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import subprocess
import os
import re
from datetime import datetime
import json

# Global variables
inventory_file = os.path.expanduser("~/ansible_projeto1/inventory")

class SuricataAnsibleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SAM - Suricata & Ansible Management")

        # Creating the Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Add tabs
        self.setup_tab = SetupTab(self)
        self.inventory_tab = InventoryTab(self)
        self.install_suricata_tab = InstallSuricata(self)
        self.suricata_logs_tab = SuricataLogs(self)
        self.custom_rules_tab = CustomRules(self)
        self.analyze_logs_tab = AnalyzeLogs(self)
        self.json_logs_tab = JSONLogs(self)

class SetupTab:
    #GUI for the Setup Tab
    def __init__(self, gui):
        self.gui = gui
        self.inventory_file = inventory_file
        self.setup_frame = ttk.Frame(gui.notebook, padding="10")
        gui.notebook.add(self.setup_frame, text="Setup")
        self.setup_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.setup_frame.grid_columnconfigure(1, weight=2, uniform="equal")

        self.setup_frame.grid_rowconfigure(0, weight=0)
        self.setup_frame.grid_rowconfigure(1, weight=0)
        self.setup_frame.grid_rowconfigure(2, weight=0)
        self.setup_frame.grid_rowconfigure(3, weight=0)
        self.setup_frame.grid_rowconfigure(4, weight=0)
        self.setup_frame.grid_rowconfigure(5, weight=0)
        self.setup_frame.grid_rowconfigure(6, weight=1)
        self.setup_frame.grid_rowconfigure(7, weight=0)

        # SSH Key Name
        self.key_name_label = tk.Label(self.setup_frame, text="SSH Key Name:")
        self.key_name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.key_name_entry = tk.Entry(self.setup_frame)
        self.key_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # SSH Key Comment
        self.comment_label = tk.Label(self.setup_frame, text="SSH Key Comment:")
        self.comment_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.comment_entry = tk.Entry(self.setup_frame)
        self.comment_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Server IPs
        self.server_ips_label = tk.Label(self.setup_frame, text="Server IPs (comma separated):")
        self.server_ips_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.server_ips_entry = tk.Entry(self.setup_frame)
        self.server_ips_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Create SSH Key Button
        self.create_key_button = tk.Button(self.setup_frame, text="Create & Copy Public SSH Key To Remote Server", command=self.create_and_copy_key)
        self.create_key_button.grid(row=3, columnspan=2, pady=10, sticky="ew")

        # Private Key Path
        private_key_label = tk.Label(self.setup_frame, text="Enter Private Key Path:")
        private_key_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.private_key_entry = tk.Entry(self.setup_frame)
        self.private_key_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Add SSH Identity Button
        self.ssh_idd_add_button = tk.Button(self.setup_frame, text="Add SSH identity", command=self.add_ssh_identity)
        self.ssh_idd_add_button.grid(row=5, columnspan=2, pady=10, sticky="ew")

        # Remote Key Path
        remote_key_path_label = tk.Label(self.setup_frame, text="Enter Remote SSH Key Path:")
        remote_key_path_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.remote_key_path_entry = tk.Entry(self.setup_frame)
        self.remote_key_path_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        # List SSH Keys Button
        self.ls_button = tk.Button(self.setup_frame, text="List Remote SSH keys", command=self.list_directory)
        self.ls_button.grid(row=7, columnspan=2, pady=10, sticky="ew")

        # SSH Keys on Remote Server
        self.ls_label = tk.Label(self.setup_frame, text="SSH Keys on the remote server:")
        self.ls_label.grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.ls_textbox = tk.Text(self.setup_frame, height=20, width=40)
        self.ls_textbox.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

    # Function to create and copy SSH key to remote server, this part cant be run on background mode because it needs user input
    def create_and_copy_key(self):
        key_name = self.key_name_entry.get()
        comment = self.comment_entry.get()
        ips = self.server_ips_entry.get()

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
                command = ["ssh-copy-id", "-i", f"{ssh_dir}{key_name}.pub", ip]
                print(f"Running command: {' '.join(command)}")  # Print the command being run
                subprocess.run(command, check=True)

            # Step 3: Create an alias for the ssh-agent setup and add it to .bashrc for persistence
            alias_command = "alias ssha='eval $(ssh-agent) && ssh-add'"
            with open(os.path.expanduser("~/.bashrc"), "a") as bashrc_file:
                bashrc_file.write(f"\n{alias_command}\n")

            # Step 4: start the ssh-agent and add the private key
            subprocess.run(f"eval $(ssh-agent) && ssh-add {ssh_dir}{key_name}", check=True, shell=True)

            # Inform the user of success
            messagebox.showinfo("Success", "SSH Key copied to servers and SSH agent configured.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
        except IOError as e:
            messagebox.showerror("Error", f"An error occurred when writing to .bashrc: {e}")



        
    #Function to list SSH keys on remote server
    def list_directory(self):
        # Get the SSH key path from the input field and expand '~' to full path
        remote_key_path = os.path.expanduser(self.remote_key_path_entry.get())

        if not remote_key_path:
            self.ls_textbox.delete("1.0", tk.END)
            self.ls_textbox.insert(tk.END, "Please enter a valid SSH key path.\n")
            return

        # Assuming self.inventory_file is already set correctly
        if not hasattr(self, 'inventory_file'):
            self.ls_textbox.delete("1.0", tk.END)
            self.ls_textbox.insert(tk.END, "Inventory file is not set.\n")
            return

        # Playbook command with the SSH key path passed as a variable
        playbook_command = [
            "ansible-playbook",
            "-i", self.inventory_file,
            "-e", f"ssh_key_path={remote_key_path}",  # Pass the expanded SSH key path
            "ls_ssh_keys.yml"
        ]

        try:
            # Execute the ansible-playbook command and capture the output
            result = subprocess.run(playbook_command, capture_output=True, text=True)

            # Check if the playbook ran successfully
            if result.returncode == 0:
                # Clear the TextBox before inserting new content
                self.ls_textbox.delete("1.0", tk.END)

                # Extract the output for each host
                output_lines = result.stdout.splitlines()
                host_key_contents = []

                for line in output_lines:
                    if '"msg":' in line:
                        # Extract the SSH key content from the "msg" line
                        key_contents = line.split('"msg":')[1].strip().strip('"')
                        host_key_contents.append(key_contents)

                if host_key_contents:
                    # Insert the SSH keys for each host into the TextBox
                    self.ls_textbox.insert(tk.END, "\n".join(host_key_contents) + "\n")
                else:
                    self.ls_textbox.insert(tk.END, "No authorized keys found or unable to access the file.")
            else:
                self.ls_textbox.delete("1.0", tk.END)
                # Show error message if the playbook failed
                self.ls_textbox.insert(tk.END, f"Error: {result.stderr}")

        except Exception as e:
            self.ls_textbox.delete("1.0", tk.END)
            self.ls_textbox.insert(tk.END, f"Exception: {str(e)}")
    
    #Function to add SSH identity, its necessary to comunicate with the remote server without password everytime we reboot the machine
    def add_ssh_identity(self):
        private_key_path = self.private_key_entry.get()  # Get private key path from input field

        # Expand '~' to the full home directory path
        private_key_path = os.path.expanduser(private_key_path)

        # Debugging print to check the input value
        print(f"Private Key Path: {repr(private_key_path)}")

        if not private_key_path:
            messagebox.showerror("Error", "Private key path must be provided.")
            return

        # Check if the private key file exists
        if not os.path.isfile(private_key_path):
            messagebox.showerror("Error", f"The private key file does not exist: {private_key_path}")
            return

        try:
            # Run the full command instead of alias
            subprocess.run(f"eval $(ssh-agent) && ssh-add {private_key_path}", check=True, shell=True)

            # Inform the user of success
            messagebox.showinfo("Success", "SSH identity added successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

class InventoryTab:
    #GUI for the Inventory Tab
    def __init__(self, gui):
        self.gui = gui
        self.inventory_file = inventory_file
        self.inventory_frame = ttk.Frame(gui.notebook, padding="10")
        gui.notebook.add(self.inventory_frame, text="Inventory")

        # Inventory IP Address
        self.inventory_ip_label = tk.Label(self.inventory_frame, text="IP Address:")
        self.inventory_ip_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.inventory_ip_entry = tk.Entry(self.inventory_frame)
        self.inventory_ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Inventory Username
        self.user_label = tk.Label(self.inventory_frame, text="Username:")
        self.user_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.user_entry = tk.Entry(self.inventory_frame)
        self.user_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Inventory Password
        self.password_label = tk.Label(self.inventory_frame, text="Password:")
        self.password_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = tk.Entry(self.inventory_frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Buttons for Inventory Management
        self.save_inventory_button = tk.Button(self.inventory_frame, text="New Server", command=self.save_server)
        self.save_inventory_button.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        self.load_inventory_button = tk.Button(self.inventory_frame, text="Load Inventory", command=self.load_inventory)
        self.load_inventory_button.grid(row=4, columnspan=2, padx=5, pady=5, sticky="ew")

        self.inventory_text = tk.Text(self.inventory_frame, height=15, width=60)
        self.inventory_text.grid(row=5, columnspan=2, padx=5, pady=5, sticky="nsew")

        self.delete_button = tk.Button(self.inventory_frame, text="Delete Server", command=self.delete_server)
        self.delete_button.grid(row=6, columnspan=2, padx=5, pady=5, sticky="ew")

        # Ensure the inventory text box expands with the window
        self.inventory_frame.grid_rowconfigure(5, weight=1)
        self.inventory_frame.grid_columnconfigure(0, weight=1)
        self.inventory_frame.grid_columnconfigure(1, weight=3)

    #Function to save server in the inventory file
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

    #Function to load inventory file
    def load_inventory(self):
        try:
            # Read the inventory file and display its contents in the text widget
            with open(self.inventory_file, "r") as file:
                inventory = file.read()

            self.inventory_text.delete(1.0, tk.END)  # Clear the current content
            self.inventory_text.insert(tk.END, inventory)  # Insert the new content
        except IOError as e:
            messagebox.showerror("Error", f"An error occurred while reading the inventory file: {e}")
    
    #Function to delete server from inventory file
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

class InstallSuricata:
    #GUI for the Install Suricata Tab
    def __init__(self, gui):
        self.gui = gui
        self.inventory_file = inventory_file
        self.install_frame = ttk.Frame(gui.notebook, padding="10")
        gui.notebook.add(self.install_frame, text="Install Suricata")

        self.run_playbook_button = tk.Button(self.install_frame, text="Install Suricata", command=self.install_suricata)
        self.run_playbook_button.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        # Enter Interface
        self.interface_label = tk.Label(self.install_frame, text="Enter Interface:")
        self.interface_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.interface_entry = tk.Entry(self.install_frame)
        self.interface_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.change_interface_button = tk.Button(self.install_frame, text="Change Interface", command=self.change_interface)
        self.change_interface_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        # Configure grid weights to ensure elements expand properly
        self.install_frame.grid_rowconfigure(0, weight=0)
        self.install_frame.grid_rowconfigure(1, weight=0)
        self.install_frame.grid_rowconfigure(2, weight=0)
        self.install_frame.grid_columnconfigure(0, weight=1)
        self.install_frame.grid_columnconfigure(1, weight=2)

    #Function to install Suricata
    def install_suricata(self):
        # Executes the Ansible playbook to install and configure Suricata 
        try:
            # Run the Ansible playbook to install Suricata
            subprocess.run([
                "ansible-playbook", "-i", self.inventory_file, "install_suricata.yml"
            ], check=True)

            # Show success message
            messagebox.showinfo("Success", "Suricata installation completed.")
        except subprocess.CalledProcessError as e:
            # Handle error
            messagebox.showerror("Error", f"An error occurred while running the playbook: {e}")
    
    #Function to change interface in the suricata.yaml file under /etc/suricata/suricata.yaml, it changes every "interface:" on the file
    def change_interface(self):
        # Get the interface from the entry field
        interface = self.interface_entry.get()

        try:
            subprocess.run(["ansible-playbook", "change_interface.yml", "-e", f"interface={interface}"], check=True)
            messagebox.showinfo("Success", "Interface changed successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

class SuricataLogs:
    #GUI for the Suricata Logs Tab
    def __init__(self, gui):
        self.gui = gui
        self.inventory_file = inventory_file
        self.logs_frame = ttk.Frame(gui.notebook, padding="10")
        gui.notebook.add(self.logs_frame, text="Suricata Fast Logs")

        # View Logs Button
        self.view_logs_button = tk.Button(self.logs_frame, text="View Logs", command=self.view_logs)
        self.view_logs_button.grid(row=0, columnspan=2, pady=10, sticky="ew")

        # Text box for displaying logs
        self.log_text = tk.Text(self.logs_frame, height=15, width=60)
        self.log_text.grid(row=1, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Ensure the logs text box expands with the window
        self.logs_frame.grid_rowconfigure(1, weight=1)
        self.logs_frame.grid_columnconfigure(0, weight=1)
        self.logs_frame.grid_columnconfigure(1, weight=3)

    #Function to view Suricata logs using an Ansible playbook
    def view_logs(self):
        # Path to your playbook
        playbook_path = os.path.expanduser("~/ansible_projeto1/read_log.yml")

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
                # Extract only the content of the fast.log file from the output
                log_content = self.extract_log_content(playbook_output)

                # Display the content of the fast.log in the text widget
                self.log_text.delete(1.0, tk.END)  # Clear the text box
                self.log_text.insert(tk.END, log_content)  # Insert the extracted log content

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Ansible playbook execution failed: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view Suricata logs: {e}")

    #Function to extract log content from the playbook output and filter it
    def extract_log_content(self, playbook_output):
        # Extract log content: We assume the log entries begin after the "msg" field
        # and end at the last log entry (matching the log format).
        
        # Find the part that contains the logs (after "msg":)
        start_index = playbook_output.find('msg":')

        if start_index != -1:
            # Extract the content after "msg": (skip the leading "msg": part)
            log_content = playbook_output[start_index + 6:].strip()  # Skip over 'msg":'
            
            # Clean up any surrounding quotes
            if log_content.startswith('"') and log_content.endswith('"'):
                log_content = log_content[1:-1]  # Remove the first and last quote marks
            
            # Replace \\n with actual newline character
            log_content = log_content.replace("\\n", "\n").strip()

            # Now filter the log content to only include lines starting with a date (e.g., xx/xx/xxxx)
            filtered_log = ""
            for line in log_content.splitlines():
                # Match lines starting with a date in the format MM/DD/YYYY (e.g., 12/13/2024)
                if re.match(r"^\d{2}/\d{2}/\d{4}", line):  # Matches date format at the start of the line
                    filtered_log += line + "\n"  # Add matching line to filtered content

            return filtered_log if filtered_log else "No logs found with valid date format."

        else:
            return "No log content found."  # In case no log content is found

class CustomRules:
    #GUI for the Custom Rules Tab
    def __init__(self, gui):
        self.gui = gui
        self.inventory_file = inventory_file
        self.rules_frame = ttk.Frame(gui.notebook, padding="10")
        gui.notebook.add(self.rules_frame, text="Custom Rules")

        # Action Dropdown
        self.action_label = tk.Label(self.rules_frame, text="Action:")
        self.action_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.action_var = tk.StringVar()
        self.action_dropdown = tk.OptionMenu(self.rules_frame, self.action_var, "alert", "pass", "drop", "reject", "log")
        self.action_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Protocol
        self.protocol_label = tk.Label(self.rules_frame, text="Protocol:")
        self.protocol_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.protocol_entry = tk.Entry(self.rules_frame)
        self.protocol_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Source IP
        self.src_ip_label = tk.Label(self.rules_frame, text="Source IP:")
        self.src_ip_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.src_ip_entry = tk.Entry(self.rules_frame)
        self.src_ip_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Source Port
        self.src_port_label = tk.Label(self.rules_frame, text="Source Port:")
        self.src_port_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.src_port_entry = tk.Entry(self.rules_frame)
        self.src_port_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Destination IP
        self.dst_ip_label = tk.Label(self.rules_frame, text="Destination IP:")
        self.dst_ip_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.dst_ip_entry = tk.Entry(self.rules_frame)
        self.dst_ip_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Destination Port
        self.dst_port_label = tk.Label(self.rules_frame, text="Destination Port:")
        self.dst_port_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.dst_port_entry = tk.Entry(self.rules_frame)
        self.dst_port_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Message
        self.msg_label = tk.Label(self.rules_frame, text="Message:")
        self.msg_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.msg_entry = tk.Entry(self.rules_frame)
        self.msg_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        # SID
        self.sid_label = tk.Label(self.rules_frame, text="SID:")
        self.sid_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.sid_entry = tk.Entry(self.rules_frame)
        self.sid_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        # Save Rule Button
        self.save_rule_button = tk.Button(self.rules_frame, text="Save Rule", command=self.save_custom_rule)
        self.save_rule_button.grid(row=8, columnspan=2, pady=10, sticky="ew")

        # View Custom Rules Button
        self.view_rules_button = tk.Button(self.rules_frame, text="View Custom Rules", command=self.view_custom_rules)
        self.view_rules_button.grid(row=9, columnspan=2, pady=10, sticky="ew")

        # Custom Rules Text Box
        self.custom_rules_text = tk.Text(self.rules_frame, height=15, width=60)
        self.custom_rules_text.grid(row=10, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Delete Rule Entry
        self.delete_rule_entry = tk.Entry(self.rules_frame)
        self.delete_rule_entry.grid(row=11, column=0, padx=5, pady=5, sticky="ew")

        # Delete Rule Button
        self.delete_rule_button = tk.Button(self.rules_frame, text="Delete Rule", command=self.delete_custom_rules)
        self.delete_rule_button.grid(row=11, column=1, padx=5, pady=5, sticky="ew")

        # Ensure the custom rules text box expands with the window
        self.rules_frame.grid_rowconfigure(10, weight=1)
        self.rules_frame.grid_columnconfigure(0, weight=1)
        self.rules_frame.grid_columnconfigure(1, weight=3)

    #Function to save custom rules
    def save_custom_rule(self):
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
            result = subprocess.run(
                ["ansible-playbook", "-i", self.inventory_file, "view_custom_rules.yml"],
                capture_output=True,
                text=True,
                check=True
            )

            # Extract the rules from Ansible output
            for line in result.stdout.splitlines():
                if "custom_rules.stdout" in line:
                    # Clean up the rules content from stdout
                    # Find the part after the "custom_rules.stdout": and remove any surrounding quotes
                    rules = line.split("custom_rules.stdout")[1].split(":", 1)[-1].strip().strip('"')

                    # Insert rules into the Text widget, preserving line breaks
                    self.custom_rules_text.delete(1.0, tk.END)  # Clear any previous content

                    # Replace any \\n with actual newline character and insert the clean rules
                    self.custom_rules_text.insert(tk.END, rules.replace("\\n", "\n"))

                    return

            # If content not found, show error
            messagebox.showerror("Error", "Failed to fetch custom rules.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_custom_rules(self):
        custom_rule_to_delete = self.delete_rule_entry.get()

        if not custom_rule_to_delete:
            messagebox.showerror("Error", "Please enter a rule to delete.")
            return

        try:
            subprocess.run([
                "ansible-playbook", "-i", self.inventory_file, "delete_custom_rule.yml", 
                "--extra-vars", f"custom_rule='{custom_rule_to_delete}'"
            ], check=True)

            # Display success message
            messagebox.showinfo("Success", "Custom rule deleted.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

class AnalyzeLogs:
    # GUI for the Analyze Logs Tab
    def __init__(self, gui):
        self.gui = gui
        self.logs = []
        self.filtered_logs = []
        self.active_filters = {}
        self.analyze_frame = ttk.Frame(gui.notebook, padding="10")
        gui.notebook.add(self.analyze_frame, text="Analyze Fast Logs")
        self.inventory_file = inventory_file

        # Create the text box to display log content
        self.log_text = tk.Text(self.analyze_frame, wrap=tk.WORD, height=15, width=80, font=("Helvetica", 12))
        self.log_text.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Button to load the log file
        self.load_button = tk.Button(self.analyze_frame, text="Load Log File", command=self.load_log_file)
        self.load_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Filter buttons
        self.filter_ip_button = tk.Button(self.analyze_frame, text="Filter by IP", command=self.filter_by_ip)
        self.filter_ip_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.filter_date_button = tk.Button(self.analyze_frame, text="Filter by Date", command=self.filter_by_date)
        self.filter_date_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.filter_protocol_button = tk.Button(self.analyze_frame, text="Filter by Protocol", command=self.filter_by_protocol)
        self.filter_protocol_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        self.clear_button = tk.Button(self.analyze_frame, text="Clear Filters", command=self.clear_filters)
        self.clear_button.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        # Sort buttons
        self.sort_asc_button = tk.Button(self.analyze_frame, text="Sort Ascending", command=lambda: self.sort_logs(ascending=True))
        self.sort_asc_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.sort_desc_button = tk.Button(self.analyze_frame, text="Sort Descending", command=lambda: self.sort_logs(ascending=False))
        self.sort_desc_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Label to display active filters
        self.active_filters_label = tk.Label(self.analyze_frame, text="Active Filters: None")
        self.active_filters_label.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="ew")

        # Configure rows and columns to expand with the window
        self.analyze_frame.grid_rowconfigure(0, weight=1)  # Make text widget expand
        self.analyze_frame.grid_rowconfigure(1, weight=0)
        self.analyze_frame.grid_rowconfigure(2, weight=0)
        self.analyze_frame.grid_rowconfigure(3, weight=0)
        self.analyze_frame.grid_rowconfigure(4, weight=0)
        self.analyze_frame.grid_columnconfigure(0, weight=1)
        self.analyze_frame.grid_columnconfigure(1, weight=1)
        self.analyze_frame.grid_columnconfigure(2, weight=1)
        self.analyze_frame.grid_columnconfigure(3, weight=1)

    # Function to load log file
    def load_log_file(self):
        # Run the Ansible playbook to fetch the fast.log file
        try:
            subprocess.run(
                ["ansible-playbook", "-i", self.inventory_file, "get_fast_log.yml"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to fetch log file: {e}")
            return

        # Automatically load the fast.log file
        file_path = os.path.expanduser("~/ansible_projeto1/fast.log")

        try:
            with open(file_path, "r") as file:
                self.logs = [line.strip() for line in file if line.strip()]
                self.filtered_logs = self.logs  # Initially, no filter, show all logs
                self.display_logs(self.filtered_logs)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load log file: {e}")

    # Function to display logs
    def display_logs(self, logs):
        self.log_text.delete(1.0, tk.END)  # Clear the text box
        if logs:
            self.log_text.insert(tk.END, '\n'.join(logs))  # Display logs in the text box
        else:
            self.log_text.insert(tk.END, "No logs to display.")

    # Function to filter logs by IP
    def filter_by_ip(self):
        ip = self.get_input("Enter IP Address to Filter by:")
        if ip:
            self.active_filters['ip'] = ip
            self.apply_filters()

    # Function to filter logs by date
    def filter_by_date(self):
        date_str = self.get_input("Enter Date (MM/DD/YYYY) to Filter by:")
        try:
            # Validate the date format
            date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            self.active_filters['date'] = date_obj
            self.apply_filters()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use MM/DD/YYYY.")

    # Function to filter logs by protocol
    def filter_by_protocol(self):
        protocol = self.get_input("Enter Protocol to Filter by:")
        if protocol:
            self.active_filters['protocol'] = protocol
            self.apply_filters()

    # Function to apply all active filters
    def apply_filters(self):
        filtered_logs = self.logs
        if 'ip' in self.active_filters:
            filtered_logs = [log for log in filtered_logs if self.active_filters['ip'] in log]
        if 'date' in self.active_filters:
            filtered_logs = [log for log in filtered_logs if self.match_date(log, self.active_filters['date'])]
        if 'protocol' in self.active_filters:
            filtered_logs = [log for log in filtered_logs if self.active_filters['protocol'].lower() in log.lower()]

        self.filtered_logs = filtered_logs
        self.display_logs(self.filtered_logs)
        self.update_active_filters_label()

    # Function to get input from user
    def get_input(self, prompt):
        input_dialog = tk.simpledialog.askstring("Input", prompt)
        return input_dialog.strip() if input_dialog else None

    # Function to match the date in the log line
    def match_date(self, log, date_obj):
        # Extract the date from the log line
        date_str = log.split('-')[0]  # The date is at the start of the log line
        try:
            log_date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            return log_date_obj.date() == date_obj.date()
        except ValueError:
            return False

    # Function to extract date from log
    def extract_date(self, log):
        date_str = log.split('-')[0].strip()
        try:
            return datetime.strptime(date_str, "%m/%d/%Y")
        except ValueError:
            return datetime.min  # Return a minimum date if parsing fails

    # Function to clear filters
    def clear_filters(self):
        self.active_filters = {}
        self.filtered_logs = self.logs  # Reset to all logs
        self.display_logs(self.filtered_logs)
        self.update_active_filters_label()

    # Function to update the active filters label
    def update_active_filters_label(self):
        if self.active_filters:
            filters_text = ", ".join([f"{key}: {value}" for key, value in self.active_filters.items()])
            self.active_filters_label.config(text=f"Active Filters: {filters_text}")
        else:
            self.active_filters_label.config(text="Active Filters: None")

    # Function to sort logs
    def sort_logs(self, ascending=True):
        try:
            self.filtered_logs.sort(key=lambda log: datetime.strptime(log.split('-')[0], "%m/%d/%Y"), reverse=not ascending)
            self.display_logs(self.filtered_logs)
        except ValueError:
            messagebox.showerror("Error", "Failed to sort logs. Ensure logs have valid date format.")

class JSONLogs:
    # GUI for the JSON Logs Tab
    def __init__(self, gui):
        self.gui = gui
        self.logs = []
        self.inventory_file = inventory_file
        self.filtered_logs = []
        self.active_filters = {}
        self.json_logs_frame = ttk.Frame(gui.notebook, padding="10")
        gui.notebook.add(self.json_logs_frame, text="Analyze JSON Logs")

        # Create the text box to display log content
        self.log_text = tk.Text(self.json_logs_frame, wrap=tk.WORD, height=15, width=80, font=("Helvetica", 12))
        self.log_text.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Button to load the log file
        self.load_button = tk.Button(self.json_logs_frame, text="Load JSON Log File", command=self.load_log_file)
        self.load_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Filter buttons
        self.filter_ip_button = tk.Button(self.json_logs_frame, text="Filter by IP", command=self.filter_by_ip)
        self.filter_ip_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.filter_date_button = tk.Button(self.json_logs_frame, text="Filter by Date", command=self.filter_by_date)
        self.filter_date_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.filter_protocol_button = tk.Button(self.json_logs_frame, text="Filter by Protocol", command=self.filter_by_protocol)
        self.filter_protocol_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        self.clear_button = tk.Button(self.json_logs_frame, text="Clear Filters", command=self.clear_filters)
        self.clear_button.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        # Sort buttons
        self.sort_asc_button = tk.Button(self.json_logs_frame, text="Sort Ascending", command=lambda: self.sort_logs(ascending=True))
        self.sort_asc_button.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        self.sort_desc_button = tk.Button(self.json_logs_frame, text="Sort Descending", command=lambda: self.sort_logs(ascending=False))
        self.sort_desc_button.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Label to display active filters
        self.active_filters_label = tk.Label(self.json_logs_frame, text="Active Filters: None")
        self.active_filters_label.grid(row=4, column=0, columnspan=4, padx=10, pady=5, sticky="ew")

        # Configure rows and columns to expand with the window
        self.json_logs_frame.grid_rowconfigure(0, weight=1)  # Make text widget expand
        self.json_logs_frame.grid_rowconfigure(1, weight=0)
        self.json_logs_frame.grid_rowconfigure(2, weight=0)
        self.json_logs_frame.grid_rowconfigure(3, weight=0)
        self.json_logs_frame.grid_rowconfigure(4, weight=0)
        self.json_logs_frame.grid_columnconfigure(0, weight=1)
        self.json_logs_frame.grid_columnconfigure(1, weight=1)
        self.json_logs_frame.grid_columnconfigure(2, weight=1)
        self.json_logs_frame.grid_columnconfigure(3, weight=1)

    # Function to load log file
    def load_log_file(self):
        # Run the Ansible playbook to fetch the JSON log file
        try:
            subprocess.run(
                ["ansible-playbook", "-i", self.inventory_file, "get_eve_json.yml"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to fetch JSON log file: {e}")
            return

        # Automatically load the eve.json file
        file_path = os.path.expanduser("~/ansible_projeto1/eve.json")

        try:
            with open(file_path, "r") as file:
                self.logs = [json.loads(line) for line in file]
                self.filtered_logs = self.logs  # Initially, no filter, show all logs
                self.display_logs(self.filtered_logs)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load log file: {e}")

    # Function to display logs
    def display_logs(self, logs):
        self.log_text.delete(1.0, tk.END)  # Clear the text box
        if logs:
            self.log_text.insert(tk.END, '\n'.join(json.dumps(log, indent=4) for log in logs))  # Display logs in the text box
        else:
            self.log_text.insert(tk.END, "No logs to display.")

    # Function to filter logs by IP
    def filter_by_ip(self):
        ip = self.get_input("Enter IP Address to Filter by:")
        if ip:
            self.active_filters['ip'] = ip
            self.apply_filters()

    # Function to filter logs by date
    def filter_by_date(self):
        date_str = self.get_input("Enter Date (MM/DD/YYYY) to Filter by:")
        try:
            # Validate the date format
            date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            self.active_filters['date'] = date_obj
            self.apply_filters()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use MM/DD/YYYY.")

    # Function to filter logs by protocol
    def filter_by_protocol(self):
        protocol = self.get_input("Enter Protocol to Filter by:")
        if protocol:
            self.active_filters['protocol'] = protocol
            self.apply_filters()

    # Function to apply all active filters
    def apply_filters(self):
        filtered_logs = self.logs
        if 'ip' in self.active_filters:
            filtered_logs = [log for log in filtered_logs if self.active_filters['ip'] in log.get('src_ip', '') or self.active_filters['ip'] in log.get('dest_ip', '')]
        if 'date' in self.active_filters:
            filtered_logs = [log for log in filtered_logs if self.match_date(log, self.active_filters['date'])]
        if 'protocol' in self.active_filters:
            filtered_logs = [log for log in filtered_logs if self.active_filters['protocol'].lower() in log.get('proto', '').lower()]

        self.filtered_logs = filtered_logs
        self.display_logs(self.filtered_logs)
        self.update_active_filters_label()

    # Function to get input from user
    def get_input(self, prompt):
        input_dialog = tk.simpledialog.askstring("Input", prompt)
        return input_dialog.strip() if input_dialog else None

    # Function to match the date in the log line
    def match_date(self, log, date_obj):
        # Extract the date from the log dictionary
        date_str = log.get('timestamp', '').split('T')[0]  # The date is at the start of the timestamp
        try:
            log_date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            return log_date_obj.date() == date_obj.date()
        except ValueError:
            return False

    # Function to clear filters
    def clear_filters(self):
        self.active_filters = {}
        self.filtered_logs = self.logs  # Reset to all logs
        self.display_logs(self.filtered_logs)
        self.update_active_filters_label()

    # Function to update the active filters label
    def update_active_filters_label(self):
        if self.active_filters:
            filters_text = ", ".join([f"{key}: {value}" for key, value in self.active_filters.items()])
            self.active_filters_label.config(text=f"Active Filters: {filters_text}")
        else:
            self.active_filters_label.config(text="Active Filters: None")

    # Function to sort logs
    def sort_logs(self, ascending=True):
        try:
            self.filtered_logs.sort(key=lambda log: datetime.strptime(log.get('timestamp', ''), "%Y-%m-%dT%H:%M:%S.%f%z"), reverse=not ascending)
            self.display_logs(self.filtered_logs)
        except ValueError:
            messagebox.showerror("Error", "Failed to sort logs. Ensure logs have valid date format.")

# ---------------------- Main Program ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SuricataAnsibleGUI(root)
    root.mainloop()
