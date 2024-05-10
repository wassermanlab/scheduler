import os
import psutil
import subprocess
import argparse

parser = argparse.ArgumentParser(description='Check for -slurm flag')
parser.add_argument('-slurm', action='store_true', help='a flag to indicate if the script is run with slurm')
args = parser.parse_args()
use_slurm = args.slurm
if (use_slurm):
    print("using slurm")
else:
    print("NOT using slurm")


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
            command = ['pipenv', 'run', 'python', script_path]
            if use_slurm:
                command.append('-slurm')
            subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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