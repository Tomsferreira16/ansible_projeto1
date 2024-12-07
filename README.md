# ansible_projeto1

## Setup Tab
- **Generate SSH Key**  
  Generates an SSH key pair for secure connections.
  
- **Add the Key**  
  Add the `key_name.pub` to the server where Suricata is installed.

- **Evaluate SSH Agent**  
  Run `eval $(ssh-agent)` to start the SSH agent.

- **Add SSH Private Key**  
  Add the private key using the command `ssh-add ~/.ssh/key_name(private)`.

- **Create Alias for SSH Agent**  
  Create an alias with the command: `alias ssha='eval $(ssh-agent) && ssh-add'`.

## Inventory Tab
- **Add a New Server**  
  Add a new server by specifying the IP address, username, and password.

- **Load Inventory File**  
  Use `cat` to load and view the inventory file.

- **Delete Server**  
  Delete a server by selecting it using the mouse.

## Install Suricata
- **Input Interface**  
  Enter the interface that Suricata will use for network monitoring.

## Suricata Logs
- **View Fast Logs**  
  View the Suricata logs at `/var/log/suricata/fast.log`.

## Custom Rules Tab
- **Add Custom Rule**  
  Add custom rules with the following parameters:
  - Action
  - Protocol
  - Source IP
  - Source Port
  - Destination IP
  - Destination Port
  - Message
  - SID

- **View Custom Rules**  
  View the custom rules stored in `/etc/suricata/rules/custom.rules`.
