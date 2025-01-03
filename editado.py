#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import subprocess
import os
import re
from datetime import datetime



class SuricataAnsibleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Suricata & Ansible Management")

        # Path to the inventory file
        self.inventory_file = os.path.expanduser("~/ansible_projeto1/inventory")

        # Creating the Notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # ---------------------- Setup Tab ----------------------
        # Create the notebook and frame
        self.setup_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.setup_frame, text="Setup")

        # Configure columns and rows to expand
        self.setup_frame.grid_columnconfigure(0, weight=1, uniform="equal")
        self.setup_frame.grid_columnconfigure(1, weight=2, uniform="equal")

        # Rows can also be configured to expand
        self.setup_frame.grid_rowconfigure(0, weight=0)  # No expansion for the first row (labels)
        self.setup_frame.grid_rowconfigure(1, weight=0)
        self.setup_frame.grid_rowconfigure(2, weight=0)
        self.setup_frame.grid_rowconfigure(3, weight=0)
        self.setup_frame.grid_rowconfigure(4, weight=1)  # Allow row with TextBox to expand
        self.setup_frame.grid_rowconfigure(5, weight=0)

        # Labels and Entries
        self.key_name_label = tk.Label(self.setup_frame, text="SSH Key Name:")
        self.key_name_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.key_name_entry = tk.Entry(self.setup_frame)
        self.key_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.comment_label = tk.Label(self.setup_frame, text="SSH Key Comment:")
        self.comment_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.comment_entry = tk.Entry(self.setup_frame)
        self.comment_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.setup_ip_label = tk.Label(self.setup_frame, text="Server IPs (comma separated):")
        self.setup_ip_label.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.setup_ip_entry = tk.Entry(self.setup_frame)
        self.setup_ip_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Create SSH Key Button
        self.create_key_button = tk.Button(self.setup_frame, text="Create & Copy Public SSH Key To Remote Server", command=self.create_and_copy_key)
        self.create_key_button.grid(row=3, columnspan=2, pady=10, sticky="ew")

          # Private Key Path Input Field
        private_key_label = tk.Label(self.setup_frame, text="Enter Private Key Path:")
        private_key_label.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.private_key_entry = tk.Entry(self.setup_frame)  # Save the reference to the input field
        self.private_key_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Add the SSH Identity button
        self.ssh_idd_add_button = tk.Button(self.setup_frame, text="Add SSH identity", command=self.add_ssh_identity)
        self.ssh_idd_add_button.grid(row=5, columnspan=2, pady=10, sticky="ew")

       # Remote SSH Key Path Input Field
        remote_key_path_label = tk.Label(self.setup_frame, text="Enter Remote SSH Key Path:")
        remote_key_path_label.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.remote_key_path_entry = tk.Entry(self.setup_frame)  # Save the reference to the input field
        self.remote_key_path_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        # TextBox and Button for ls_ssh_keys
        self.ls_label = tk.Label(self.setup_frame, text="SSH Keys on the remote server:")
        self.ls_label.grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.ls_textbox = tk.Text(self.setup_frame, height=20, width=40)
        self.ls_textbox.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        self.ls_button = tk.Button(self.setup_frame, text="List SSH keys", command=self.list_directory)
        self.ls_button.grid(row=8, columnspan=2, pady=10, sticky="ew")



        # ---------------------- Inventory Tab ----------------------
        self.inventory_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.inventory_frame, text="Inventory")

        self.inventory_ip_label = tk.Label(self.inventory_frame, text="IP Address:")
        self.inventory_ip_label.grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.inventory_ip_entry = tk.Entry(self.inventory_frame)
        self.inventory_ip_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.user_label = tk.Label(self.inventory_frame, text="Username:")
        self.user_label.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.user_entry = tk.Entry(self.inventory_frame)
        self.user_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

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

        # ---------------------- Install Suricata Tab ----------------------
        self.install_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.install_frame, text="Install Suricata")

        self.run_playbook_button = tk.Button(self.install_frame, text="Install Suricata", command=self.install_suricata)
        self.run_playbook_button.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")

        self.interface_label = tk.Label(self.install_frame, text="Enter Interface:")
        self.interface_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.interface_entry = tk.Entry(self.install_frame)
        self.interface_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.change_interface_button = tk.Button(self.install_frame, text="Change Interface", command=self.change_interface)
        self.change_interface_button.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        # Configure grid weights to ensure elements expand properly
        self.install_frame.grid_columnconfigure(0, weight=1)
        self.install_frame.grid_columnconfigure(1, weight=2)

        # ---------------------- Suricata Logs Tab ----------------------
        # Define the logs_frame and its contents
        self.logs_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.logs_frame, text="Suricata Logs")

        # View Logs Button
        self.view_logs_button = tk.Button(self.logs_frame, text="View Logs", command=self.view_logs)
        self.view_logs_button.grid(row=0, columnspan=2, pady=10, sticky="ew")

        # Text box for displaying logs
        self.log_text = tk.Text(self.logs_frame, height=15, width=60)
        self.log_text.grid(row=1, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Export Logs Button for TXT
        self.export_button = tk.Button(self.logs_frame, text="Export Logs to TXT", command=self.export_logs_to_txt)
        self.export_button.grid(row=2, columnspan=2, pady=10, sticky="ew")


        # Ensure the logs text box expands with the window
        self.logs_frame.grid_rowconfigure(1, weight=1)
        self.logs_frame.grid_columnconfigure(0, weight=1)
        self.logs_frame.grid_columnconfigure(1, weight=3)


    # ---------------------- Custom Rules Tab ----------------------
        self.rules_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.rules_frame, text="Custom Rules")

        self.action_label = tk.Label(self.rules_frame, text="Action:")
        self.action_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.action_var = tk.StringVar()
        self.action_dropdown = tk.OptionMenu(self.rules_frame, self.action_var, "alert", "pass", "drop", "reject", "log")
        self.action_dropdown.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.protocol_label = tk.Label(self.rules_frame, text="Protocol:")
        self.protocol_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.protocol_entry = tk.Entry(self.rules_frame)
        self.protocol_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.src_ip_label = tk.Label(self.rules_frame, text="Source IP:")
        self.src_ip_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.src_ip_entry = tk.Entry(self.rules_frame)
        self.src_ip_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.src_port_label = tk.Label(self.rules_frame, text="Source Port:")
        self.src_port_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.src_port_entry = tk.Entry(self.rules_frame)
        self.src_port_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        self.dst_ip_label = tk.Label(self.rules_frame, text="Destination IP:")
        self.dst_ip_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.dst_ip_entry = tk.Entry(self.rules_frame)
        self.dst_ip_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.dst_port_label = tk.Label(self.rules_frame, text="Destination Port:")
        self.dst_port_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.dst_port_entry = tk.Entry(self.rules_frame)
        self.dst_port_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        self.msg_label = tk.Label(self.rules_frame, text="Message:")
        self.msg_label.grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.msg_entry = tk.Entry(self.rules_frame)
        self.msg_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        self.sid_label = tk.Label(self.rules_frame, text="SID:")
        self.sid_label.grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.sid_entry = tk.Entry(self.rules_frame)
        self.sid_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        self.add_rule_button = tk.Button(self.rules_frame, text="Add Rule", command=self.add_rule)
        self.add_rule_button.grid(row=8, columnspan=2, pady=10, sticky="ew")

        self.view_custom_rules_button = tk.Button(self.rules_frame, text="View Custom Rules", command=self.view_custom_rules)
        self.view_custom_rules_button.grid(row=9, columnspan=2, pady=5, sticky="ew")

        # Adding input box for custom rule to delete
        self.delete_rule_label = tk.Label(self.rules_frame, text="Custom Rule to Delete:")
        self.delete_rule_label.grid(row=10, column=0, padx=5, pady=5, sticky="w")

        self.delete_rule_entry = tk.Entry(self.rules_frame)
        self.delete_rule_entry.grid(row=10, column=1, padx=5, pady=5, sticky="ew")

        self.delete_custom_rules_button = tk.Button(self.rules_frame, text="Delete Custom Rule", command=self.delete_custom_rules)
        self.delete_custom_rules_button.grid(row=11, columnspan=2, pady=5, sticky="ew")

        # Adding custom rules text box below the delete button
        self.custom_rules_text = tk.Text(self.rules_frame, height=15, width=60)
        self.custom_rules_text.grid(row=12, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Ensure the custom rules text box expands with the window
        self.rules_frame.grid_rowconfigure(12, weight=1)  # Allow row 12 to expand
        self.rules_frame.grid_columnconfigure(0, weight=1)
        self.rules_frame.grid_columnconfigure(1, weight=3)

    # ---------------------- Analyze Logs Tab ----------------------

     # Create the analyze tab
        self.analyze_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.analyze_frame, text="Analyze Logs")

        # Create the text box to display log content
        self.log_text = tk.Text(self.analyze_frame, wrap=tk.WORD, height=15, width=80, font=("Helvetica", 12))
        self.log_text.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        # Button to load the log file
        self.load_button = tk.Button(self.analyze_frame, text="Load Log File", command=self.load_log_file, font=("Helvetica", 12))
        self.load_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        # Filter buttons
        self.filter_ip_button = tk.Button(self.analyze_frame, text="Filter by IP", command=self.filter_by_ip, font=("Helvetica", 12))
        self.filter_ip_button.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        self.filter_date_button = tk.Button(self.analyze_frame, text="Filter by Date", command=self.filter_by_date, font=("Helvetica", 12))
        self.filter_date_button.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        self.filter_protocol_button = tk.Button(self.analyze_frame, text="Filter by Protocol", command=self.filter_by_protocol, font=("Helvetica", 12))
        self.filter_protocol_button.grid(row=2, column=2, padx=10, pady=5, sticky="ew")

        self.clear_button = tk.Button(self.analyze_frame, text="Clear Filters", command=self.clear_filters, font=("Helvetica", 12))
        self.clear_button.grid(row=2, column=3, padx=10, pady=5, sticky="ew")

        # Configure rows and columns to expand with the window
        self.analyze_frame.grid_rowconfigure(0, weight=1)  # Make text widget expand
        self.analyze_frame.grid_rowconfigure(1, weight=0)
        self.analyze_frame.grid_rowconfigure(2, weight=0)
        self.analyze_frame.grid_columnconfigure(0, weight=1)
        self.analyze_frame.grid_columnconfigure(1, weight=1)
        self.analyze_frame.grid_columnconfigure(2, weight=1)
        self.analyze_frame.grid_columnconfigure(3, weight=1)
        

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

    # ------------------- list the ssh keys ---------------------------------
    

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

        #------------------------Add SSH Identity ---------------
    def add_ssh_identity(self):
        private_key_path = self.private_key_entry.get()  # Get private key path from input field

        # Expand '~' to the full home directory path
        private_key_path = os.path.expanduser(private_key_path)

        # Debugging print to check the input value
        print(f"Private Key Path: {private_key_path}")

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
            messagebox.showinfo("Success", f"SSH key {private_key_path} added to the agent successfully.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred while adding the SSH key: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}") 
    
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
    #---------------------------Change Interface -----------------------------------
    def change_interface(self):
        # Get the interface from the entry field
        interface = self.interface_entry.get()

        if interface:
            # Run the change_interface.yml playbook with the selected interface as a variable
            subprocess.run(["ansible-playbook", "change_interface.yml", "-e", f"interface={interface}"])
        else:
            print("Please enter a valid interface.")


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
                # Extract only the content of the fast.log file from the output
                log_content = self.extract_log_content(playbook_output)

                # Display the content of the fast.log in the text widget
                self.log_text.delete(1.0, tk.END)  # Clear the text box
                self.log_text.insert(tk.END, log_content)  # Insert the extracted log content

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Ansible playbook execution failed: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to view Suricata logs: {e}")

    import re

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
        
    def export_logs_to_txt(self):
        # Get the log content from the text widget
        log_content = self.log_text.get(1.0, tk.END).strip()

        # Check if there is any log content
        if log_content:
            try:
                # Create a text file and write the log content into it
                with open("/home/tomas/ansible_projeto1/suricata_logs.txt", "w") as txt_file:
                    txt_file.write(log_content)
                
                messagebox.showinfo("Success", "Logs exported to TXT successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export logs to TXT: {e}")
        else:
            messagebox.showwarning("Warning", "No log content to export.")







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
            messagebox.showerror("Error", "Failed to retrieve custom rules.")

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def delete_custom_rules(self):
        custom_rule_to_delete = self.delete_rule_entry.get()

        if not custom_rule_to_delete:
            messagebox.showerror("Error", "Please enter a rule to delete.")
            return

        # Run Ansible playbook to delete the custom rule
        try:
            subprocess.run([
                "ansible-playbook", "-i", self.inventory_file, "delete_custom_rule.yml", 
                "--extra-vars", f"custom_rule='{custom_rule_to_delete}'"
            ], check=True)

            # Display success message
            messagebox.showinfo("Success", "Custom rule deleted.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # ---------------------- Analyze Logs ----------------------
     # Initialize log data variables
        self.logs = []
        self.filtered_logs = []

    def load_log_file(self):
        # Open file dialog to load the .txt log file
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not file_path:
            return

        try:
            with open(file_path, "r") as file:
                self.logs = file.readlines()
                self.filtered_logs = self.logs  # Initially, no filter, show all logs
                self.display_logs(self.filtered_logs)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load log file: {e}")

    def display_logs(self, logs):
        self.log_text.delete(1.0, tk.END)  # Clear the text box
        if logs:
            self.log_text.insert(tk.END, ''.join(logs))  # Display logs in the text box
        else:
            self.log_text.insert(tk.END, "No logs to display.")

    def filter_by_ip(self):
        ip = self.get_input("Enter IP Address to Filter by:")
        if ip:
            filtered_logs = [log for log in self.logs if ip in log]
            self.filtered_logs = filtered_logs
            self.display_logs(self.filtered_logs)

    def filter_by_date(self):
        date_str = self.get_input("Enter Date (MM/DD/YYYY) to Filter by:")
        try:
            # Validate the date format
            date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            filtered_logs = [log for log in self.logs if self.match_date(log, date_obj)]
            self.filtered_logs = filtered_logs
            self.display_logs(self.filtered_logs)
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use MM/DD/YYYY.")

    def filter_by_protocol(self):
        protocol = self.get_input("Enter Protocol to Filter by:")
        if protocol:
            filtered_logs = [log for log in self.logs if protocol.lower() in log.lower()]
            self.filtered_logs = filtered_logs
            self.display_logs(self.filtered_logs)

    def get_input(self, prompt):
        input_dialog = tk.simpledialog.askstring("Input", prompt)
        return input_dialog.strip() if input_dialog else None

    def match_date(self, log, date_obj):
        # Extract the date from the log string (assuming the date format is MM/DD/YYYY)
        date_str = log.split()[0]  # The date is at the start of the log line
        try:
            log_date_obj = datetime.strptime(date_str, "%m/%d/%Y")
            return log_date_obj.date() == date_obj.date()
        except ValueError:
            return False

    def clear_filters(self):
        self.filtered_logs = self.logs  # Reset to all logs
        self.display_logs(self.filtered_logs)

            

# ---------------------- Main Program ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = SuricataAnsibleGUI(root)
    root.mainloop()