from flask import Flask, request, jsonify, render_template
import subprocess

app = Flask(__name__)

# List of your containers
SERVERS = ["kingmc", "moviemc", "springmc", "trraria", "ciaranvs"]

@app.route('/')
def home():
    return render_template('index.html')

# Function to run docker exec inside the container
def run_linuxgsm_command(server, command):
    try:
        result = subprocess.check_output(
            f"docker exec {server} gosu linuxgsm ./{server} {command}",
            shell=True, stderr=subprocess.STDOUT, text=True
        )
        return result
    except subprocess.CalledProcessError as e:
        return e.output

@app.route('/command/<server>/<action>', methods=['POST'])
def command_server(server, action):
    if server not in SERVERS:
        return "Invalid server name", 404
 
    # Map of actions to LinuxGSM actions
    action_map = {
        "start": "start",
        "stop": "stop",
        "restart": "restart",
        "monitor": "monitor",
        "details": "details",
        "update": "update"
    }

    if action not in action_map:
        return "Invalid action", 400

    linuxgsm_command = action_map[action]
    output = run_linuxgsm_command(server, linuxgsm_command)
    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
