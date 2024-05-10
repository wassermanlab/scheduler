import os
import psutil
import subprocess

def is_running(script_path):
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['cmdline'] is not None and script_path in ' '.join(process.info['cmdline']):
            return True
    return False

def run_script(script_path):
    if not is_running(script_path):
        subprocess.Popen(['pipenv', 'run', 'python', script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        print("it's already running so i won't start a new one")

# Get the directory of the current script
current_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to start.py
start_script_path = os.path.join(current_dir, 'start.py')

run_script(start_script_path)
print("done checking that it is running")