# Suricata & Ansible Management

This project provides a graphical user interface (GUI) for managing Suricata and Ansible configurations. The application is built using Python's Tkinter library and integrates with Ansible playbooks to perform various tasks such as installing Suricata, managing inventory, viewing logs, and handling custom rules.

## Features

- **Inventory Management**: Add, load, and delete servers from the inventory.
- **Install Suricata**: Install and configure Suricata on remote servers.
- **View Suricata Logs**: View and export Suricata logs.
- **Custom Rules Management**: Add, view, and delete custom Suricata rules.
- **Analyze Logs**: Load and filter log files by IP, date, and protocol.

## Prerequisites

- Python 3.x
- Tkinter
- Ansible

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/ansible_projeto1.git
    cd ansible_projeto1
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Ensure Ansible is installed:
    ```sh
    sudo apt-get update
    sudo apt-get install ansible
    ```

## Usage

1. Run the application:
    ```sh
    python SAM.py
    ```

2. Use the GUI to manage your Suricata and Ansible configurations.

## Ansible Playbooks

The following playbooks are included in the project:

- **install_suricata.yml**: Installs and configures Suricata.
- **read_log.yml**: Reads the Suricata `fast.log` file.
- **ls_ssh_keys.yml**: Lists SSH keys on remote servers.
- **add_custom_rule.yml**: Adds a custom Suricata rule.
- **delete_custom_rule.yml**: Deletes a custom Suricata rule.
- **view_custom_rules.yml**: Views custom Suricata rules.
- **change_interface.yml**: Changes the network interface in the Suricata configuration.

## File Structure

```
ansible_projeto1/
├── SAM.py
├── inventory
├── install_suricata.yml
├── read_log.yml
├── ls_ssh_keys.yml
├── add_custom_rule.yml
├── delete_custom_rule.yml
├── view_custom_rules.yml
├── change_interface.yml
└── README.md
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
