import os
import psutil
import subprocess

def is_running(script_path):
    script_name = os.path.basename(script_path)
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.info['cmdline'] is not None:
            cmdline = ' '.join(process.info['cmdline'])
            if script_path in cmdline or script_name in cmdline:
                return True
    return False

def run_script(script_path):
    if not is_running(script_path):
        try:
            subprocess.Popen(['pipenv', 'run', 'python', script_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Started the scheduling script")
        except Exception as e:
            print(f"Error starting script: {e}")
    else:
        print("it's already running so i won't start a new one")

# Get the directory of the current script
current_dir = os.path.dirname(os.path.realpath(__file__))

# Construct the full path to start.py
start_script_path = os.path.join(current_dir, 'run-wasserman-lab-scheduled-jobs.py')

run_script(start_script_path)
print("done checking that it is running")