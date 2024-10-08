#!/bin/bash

#SBATCH --job-name=get-times      # Job name
#SBATCH --output=times_%j.out  # Output file
#SBATCH --error=times_%j.err    # Error file
#SBATCH --qos=default # QoS level
#SBATCH --ntasks=1                 # Number of tasks (1 task per simulation)
#SBATCH --cpus-per-task=1          # Number of CPU cores per task
#SBATCH --time=00:05:00           # Max time (hh:mm:ss)
#SBATCH --partition=cpu       # Specify the partition/queue
#SBATCH --account=p200503 # Account

# Get the SLURM_ARRAY_JOB_ID as an argument
array_job_id=$1
OUTPUTDIR=$2
mkdir -p $OUTPUTDIR

# Sleep for 10 seconds to ensure the array job has been recorded
sleep 10
# Fetch system and user times for all array jobs using sacct
total_user_cpu=$(sacct -j "$array_job_id" --format=JobID,JobName,Start,End,UserCPU,SystemCPU,Elapsed,TotalCPU,State --parsable2)
efficiency=$(sacct -j "$array_job_id" --format=JobID,JobName,NNodes,ReqCPUS,AllocCPUS,MaxRSS,MaxVMSize,MaxDiskRead,MaxDiskWrite,State --parsable2)

echo "$total_user_cpu" >$OUTPUTDIR/cpu_times.csv
echo "$efficiency" >$OUTPUTDIR/allocation.csv
echo "Array job $array_job_id is documented in $OUTPUTDIR/{cpu_times.csv,allocation.csv}"
