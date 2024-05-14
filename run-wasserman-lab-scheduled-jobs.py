import os
import schedule
import time
import subprocess
import logging
import datetime
import atexit
import signal
import argparse

parser = argparse.ArgumentParser(description='Check for -slurm flag')
parser.add_argument('-slurm', action='store_true', help='a flag to indicate if the script is run with slurm')
args = parser.parse_args()
use_slurm = args.slurm
if (use_slurm):
    print("scripts will be run using slurm")
else:
    print("scripts will not be run using slurm")



script_file = os.path.abspath(__file__)
print(f"script_file: {script_file}")
script_dir = os.path.dirname(script_file)
print(f"script_dir: {script_dir}")


logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.FileHandler(os.path.join(script_dir,'output.log'))
handler.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(handler)
logger.addHandler(console_handler)


# Function to execute the given shell script
def execute_script(script_path):
    try:
        if use_slurm:
            subprocess.run(['sbatch', script_path], check=True,  cwd=os.path.join(script_dir, 'workspace'))
        else:
            subprocess.run(['bash', script_path], check=True, cwd=os.path.join(script_dir, 'workspace'))
#        logging.info(f'Successfully executed {script_path}')
    except subprocess.CalledProcessError as e:
        logging.error(f'Execution of {script_path} failed with error: {e}')

already_scheduled = {}

def scan_and_schedule(folder, day_of_month='1', day_of_week='wednesday', time_of_day='12:34'):
    full_path = os.path.join(script_dir, folder)
    for file in os.listdir(full_path):
        if file.endswith('.sh'):
            script_path = os.path.join(full_path, file)
            if script_path in already_scheduled:
                continue
            job = None
            if folder == 'every-minute':
                job = schedule.every(10).seconds.do(execute_script, script_path)
                execute_script(script_path)
            elif folder == 'daily':
                job = schedule.every().day.at(time_of_day).do(
                    execute_script, script_path)
            elif folder == 'weekly':
                job = getattr(schedule.every(), day_of_week).at(time_of_day).do(
                    execute_script, script_path)
            elif folder == 'monthly':
                job = schedule.every(int(day_of_month)).days.at(time_of_day).do(
                    execute_script, script_path)
                
            already_scheduled[script_path] = job
            logger.info(f'Scheduled {script_path}')
        
def check_for_deleted_scripts():
    for script_path in list(already_scheduled.keys()):
        if not os.path.exists(script_path):
            logging.info(f"Cancel {script_path}")
            schedule.cancel_job(already_scheduled[script_path])
            del already_scheduled[script_path]

start_time = datetime.datetime.now()
logging.info(f"starting scheduler")

Running = True
def exit_handler(signal=None, stack_frame=None):
    global Running
    now = datetime.datetime.now()
    ran_for = now - start_time
    logger.info(f"Exiting scheduler. It ran for this long: {ran_for}")
    Running = False

#atexit.register(exit_handler)
signal.signal(signal.SIGTERM, exit_handler)
signal.signal(signal.SIGINT, exit_handler)

try:
    while Running:
            
        scan_and_schedule('every-minute')
        scan_and_schedule('daily')
        scan_and_schedule('weekly')
        scan_and_schedule('monthly')
        schedule.run_pending()
        check_for_deleted_scripts()
        time.sleep(10)

except Exception as e:
    logging.error(e)
    pass
