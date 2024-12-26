# Suricata Ansible GUI

This project provides a graphical user interface (GUI) for managing Suricata security tools, SSH key configurations, and Ansible playbooks. The application allows users to manage SSH keys, interact with an Ansible inventory, install Suricata, configure network interfaces, view and manage Suricata logs, and add/remove custom rules. The tool integrates with various Ansible playbooks to automate the installation and configuration process.

## Features

- **Create and Copy SSH Keys**: Generate new SSH keys or use existing ones, copy the public key to remote servers, and configure the SSH agent.
- **List SSH Keys**: Retrieve and display authorized SSH keys from remote servers using Ansible.
- **Add SSH Identity**: Add a private SSH key to the SSH agent for secure connections.
- **Manage Ansible Inventory**: Add, load, and delete servers from an Ansible inventory file.
- **Install Suricata**: Automatically install Suricata on remote servers via Ansible playbooks.
- **Change Network Interface**: Modify the monitored network interface on Suricata on the remote servers using Ansible playbooks.
- **View Suricata Logs**: Retrieve and display Suricata logs (e.g., `fast.log`) from remote servers.
- **Add Custom Rules**: Add, view, and delete custom Suricata rules for enhanced security monitoring.
- **Suricata Log Analysis**: Extract and display relevant log content from Suricata logs, filtered by date.

## Requirements

- Python 3.x
- Tkinter (for the GUI)
- Ansible (for automation)
- Suricata installed on the remote servers
- SSH access to remote servers
- Properly configured inventory file for Ansible

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/suricata-ansible-gui.git
   cd suricata-ansible-gui
