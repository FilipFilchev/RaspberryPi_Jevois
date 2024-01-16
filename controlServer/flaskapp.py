# pip install Flask Flask-SocketIO paramiko

from flask import Flask, jsonify, request
from flask_cors import CORS
import paramiko

app = Flask(__name__)
CORS(app)

def ssh_execute_command(command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("raspberrypi.local", port=22, username="pi", password="pass")

    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode()

    ssh.close()
    return output

@app.route('/start_mission', methods=['POST'])
def start_mission():
    command = "DISPLAY=:0 xmessage 'Hello from the GCS' "
    
    try:
        print("STARTING MISSION")
        # Replace 'ls' with your actual command to start the drone mission
        output = ssh_execute_command(command)
        return jsonify({'status': 'Mission successfully started', 'output': output}), 200
    except Exception as e:
        return jsonify({'status': 'Error', 'error': str(e)}), 500

@app.route('/home')
def home():
    return jsonify(message="Hello World! Welcome to my post requests pi communication server")

if __name__ == '__main__':
    app.run(debug=True)


"""Mission Status: Mission successfully started - Backgrounds box86 CommanderPi Desktop"""

