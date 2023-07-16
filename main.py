from flask import Flask, render_template, request
from subprocess import Popen, PIPE

app = Flask(__name__)

# Create a subprocess and store it in a global variable
# so that it can be accessed by the button handler function
proc = Popen(["python", "-u", "benchmark _mod.py"], stdout=PIPE)

@app.route("/")
def home():
    # Render a page with a button, an output area, and an input field
    return render_template("home.html")

@app.route("/pause_or_continue", methods=["POST"])
def pause_or_continue():
    # Check whether the subprocess is currently running or paused
    if proc.poll() is None:
        # If the subprocess is running, pause it by sending the "SIGSTOP" signal
        proc.send_signal(19)
    else:
        # If the subprocess is paused, continue it by sending the "SIGCONT" signal
        proc.send_signal(18)
    return "OK"

@app.route("/send_name", methods=["POST"])
def send_name():
    # Get the name from the input field and send it to the subprocess
    name = request.form.get("name")
    proc.stdin.write(bytes(name + "\n", "utf-8"))
    proc.stdin.flush()
    return "OK"

@app.route("/get_output", methods=["GET"])
def get_output():
    # Read the latest output from the subprocess and return it
    out = proc.stdout.readline().decode("utf-8")
    return out

@app.route("/")
def run_command():

    # Print the output of the "ls" command
    while True:
        output = proc.stdout.readline()
        if output == b'' and proc.poll() is not None:
            break
        if output:
            print(output.strip().decode())
    return "Command run successfully"

if __name__ == "__main__":
    app.run()
