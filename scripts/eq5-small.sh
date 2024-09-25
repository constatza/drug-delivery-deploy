#!/bin/bash

#SBATCH --job-name=montecarlo      # Job name
#SBATCH --qos=test              # QoS level
#SBATCH --output=../Output/slurm/montecarlo_%A.out # Output file
#SBATCH --error=../Output/slurm/montecarlo_%A.err  # Error file
#SBATCH --ntasks=1                 # Number of tasks (1 task per simulation)
#SBATCH --cpus-per-task=8          # Number of CPU cores per task
#SBATCH --time=00:00:40            # Max time (hh:mm:ss)
#SBATCH --partition=cpu        # Specify the partition/queue
#SBATCH --array=0-9%3               # Job array for 100 different parameter sets (Monte Carlo instances)
#SBATCH --account=p200503 # Account


CONFIGNAME=5EquationsSmall
OUTDIR=../Output/$CONFIGNAME/
DISTRIBUTIONPATH=../config/distributions-5.yaml
TEMPLATEPATH=../config/$CONFIGNAME.xml
CONFIGPATH=../config-auto-generated/$CONFIGNAME


# Create a virtual environment and install the required Python packages
if [ ! -d "myenv" ]; then
# if myenv does not exist, create it
    python3 -m venv myenv
    source myenv/bin/activate
    pip install pyyaml
fi
source myenv/bin/activate

# Record the start time for tracking wall time
start_time=$(date +%s)

# Run the .NET application with different inputs for each task in the job array
# Assuming your .NET app is called `MyMonteCarloApp` and takes input parameters via the command line
echo "Running task $SLURM_ARRAY_TASK_ID with number of cores: $SLURM_CPUS_PER_TASK"
python3 generate_configs.py "$DISTRIBUTIONPATH" --template "$TEMPLATEPATH"
../app/DrugDeliveryModel "$CONFIGPATH"_"$SLURM_ARRAY_TASK_ID".xml

# Record the end time
end_time=$(date +%s)

# Compute wall time in seconds
wall_time=$((end_time - start_time))

# Save timing information for later analysis
echo "Task $SLURM_ARRAY_TASK_ID: Wall time = ${wall_time} seconds" >> $OUTDIR/timing_results.txt
