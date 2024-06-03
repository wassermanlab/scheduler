#!/bin/bash

# Get the process IDs of the Python script
#pids=$(pgrep -f run-wasserman-lab-scheduled-jobs.py)
pids=$(pgrep -f "run-wasserman-lab-scheduled-jobs.py.*$")

echo "found PIDs: $pids"

# Convert the PIDs to an array
IFS=$'\n' read -d '' -r -a pid_array <<< "$pids"

for pid in "${pid_array[@]}"; do
    if [[ -n $pid ]]; then
        # Use ps to get information about the process
        echo "process information (ps) for PID $pid:";
        ps -p $pid -o pid,vsz,rss,pcpu,pmem,cmd;
        echo "process information (top) for PID $pid:";
        # Use top to get information about the process
        # Note: This will only output one snapshot of the process's usage
        top -b -n 1 -p $pid;
    else
        echo "The script is not currently running."
    fi
done





