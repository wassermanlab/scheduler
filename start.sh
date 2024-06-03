#!/bin/bash


#nohup pipenv install && pipenv run python run-wasserman-lab-scheduled-jobs.py -slurm 2>&1 &
nohup conda run -n scheduled-jobs -vvv python ./run-wasserman-lab-scheduled-jobs.py -slurm 2>&1 &

echo "did start the scheduler - pid $!"


