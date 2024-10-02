#../Output/%x/%x_%a/
def generate_array_script(job_name,
                          num_array_jobs,
                          qos="test",
                          walltime="06:00:00",
                          partition="cpu",
                          num_cores=64,
                          account="p200503",
                          initial_job_id=0
                          ):
    script_content = f"""#!/bin/bash
#SBATCH --job-name={job_name} # Job name
#SBATCH --qos={qos} # QoS level
#SBATCH --output=out # Output file
#SBATCH --error=err  # Error file
#SBATCH --ntasks=1 # Number of tasks (1 task per simulation)
#SBATCH --cpus-per-task={num_cores} # Number of CPU cores per task
#SBATCH --time={walltime} # Time limit hrs:min:sec
#SBATCH --partition={partition}  # Specify the partition/queue
#SBATCH --array={initial_job_id:d}-{initial_job_id+num_array_jobs-1:d}  # Job array for {num_array_jobs} different parameter sets (Monte Carlo instances)
#SBATCH --account={account} # Account

CONFIGPATH=../config-auto-generated/$SLURM_JOB_NAME

mkdir -p ../Output/"$SLURM_JOB_NAME"/"$SLURM_JOB_NAME"_"$SLURM_ARRAY_TASK_ID"
# Run the .NET application with different inputs for each task in the job array
echo "Running Simulation $SLURM_ARRAY_TASK_ID with number of cores: $SLURM_CPUS_PER_TASK"
../app/DrugDeliveryModel "$CONFIGPATH"_"$SLURM_ARRAY_TASK_ID".xml

echo "Simulation $SLURM_ARRAY_TASK_ID completed."
"""

    return script_content
