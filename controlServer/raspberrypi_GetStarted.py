import subprocess

def execute_remote_command(command, host="pi@yourip"): #or pi@raspberrypi.local
    try:
        result = subprocess.run(["ssh", host, command], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e.stderr.decode()}")
        return None

# Example Command: Open Chromium Browser on Raspberry Pi
#command = "DISPLAY=:0 chromium-browser"
command = "DISPLAY=:0 xmessage 'Hello from your GCS!' "

output = execute_remote_command(command)
print(output)
