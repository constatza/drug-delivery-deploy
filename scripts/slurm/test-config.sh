#!/bin/bash

#SBATCH --job-name=montecarlo      # Job name
#SBATCH --qos=test              # QoS level
#SBATCH --output=../Output/slurm/montecarlo_%A.out # Output file
#SBATCH --error=../Output/slurm/montecarlo_%A.err  # Error file
#SBATCH --ntasks=1                 # Number of tasks (1 task per simulation)
#SBATCH --cpus-per-task=1          # Number of CPU cores per task
#SBATCH --time=00:00:40            # Max time (hh:mm:ss)
#SBATCH --partition=cpu        # Specify the partition/queue
#SBATCH --array=0-3               # Job array for 100 different parameter sets (Monte Carlo instances)
#SBATCH --account=p200503 # Account

# Create a virtual environment and install the required Python packages
if [ ! -d "myenv" ]; then
# if myenv does not exist, create it
    python3 -m venv myenv
    source myenv/bin/activate
    pip install pyyaml
fi
source myenv/bin/activate

# Run the .NET application with different inputs for each task in the job array
# Assuming your .NET app is called `MyMonteCarloApp` and takes input parameters via the command line
#../app/DrugDeliveryModel ../config-auto-generated_$SLURM_ARRAY_TASK_ID.xml
sleep 10
python3 -c "import pyyaml; print('Hello from Python!')" >> ../Output/test.out

