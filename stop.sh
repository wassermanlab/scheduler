#!/bin/bash

# Get the process ID of the Python script
#pid=$(pgrep -f run-wasserman-lab-scheduled-jobs.py)
pid=$(pgrep -f "run-wasserman-lab-scheduled-jobs.py.*$")

if [[ -n $pid ]]; then
    # Send the SIGINT signal
    kill -INT $pid
    echo "Sent SIGINT signal to stop the scheduler."
else
    echo "The script is not currently running."
fi
