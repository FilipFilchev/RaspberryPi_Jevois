import paramiko

def execute_ssh_command(host, port, username, password, command):
    # Establish an SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the Raspberry Pi
        ssh.connect(host, port=port, username=username, password=password)

        # Execute the command
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.readlines()
        error = stderr.readlines()

        # Close the connection
        ssh.close()

        return output, error

    except Exception as e:
        print(f"Connection failed: {e}")
        return None, None

# Example usage
host = "raspberrypi.local" # Change to your Raspberry Pi's IP or hostname
port = 22
username = "pi" # Change to your username
password = "password" # Change to your password
command = "ls" # Example command

output, error = execute_ssh_command(host, port, username, password, command)
if output:
    print("Output:", output)
if error:
    print("Error:", error)
