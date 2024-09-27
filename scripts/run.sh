#!/bin/bash

DISTRIBUTIONPATH=$1
ANALYSISNAME=$(basename -s .yaml "$DISTRIBUTIONPATH")
OUTPUTDIR=../Output/"$ANALYSISNAME"

mkdir -p "$OUTPUTDIR"
rm -f "$OUTPUTDIR"/*.txt

# Create a virtual environment and install the required Python packages
if [ ! -d "myenv" ]; then
# if myenv does not exist, create it
    python3 -m venv myenv
    source myenv/bin/activate
    pip install pyyaml
fi
source myenv/bin/activate
slurm_input_path=$(python3 generate_configs.py "$DISTRIBUTIONPATH")

echo "Slurm file path: $slurm_input_path"
# Submit the array job and capture the job ID
array_job_output=$(sbatch "$slurm_input_path")
array_job_id=$(echo "$array_job_output" | awk '{print $4}')

OUTPUT_FILE="$OUTPUTDIR"/monitor_"$array_job_id".txt

echo "Array job submitted." > $OUTPUT_FILE
echo "ID: $array_job_id" >> $OUTPUT_FILE
echo "Time: $(date)" >> $OUTPUT_FILE

# Submit the monitoring job with a dependency on the array job
monitor_job_output=$(sbatch --dependency=afterany:$array_job_id ./slurm/get-times.sh $array_job_id)
monitor_job_ID=$(echo "$monitor_job_output" | awk '{print $4}')

echo "Monitoring Job ID: $monitor_job_ID" >> $OUTPUT_FILE
