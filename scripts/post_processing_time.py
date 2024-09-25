import os
import re

def parse_time_report(file):
    """Parse the time report file to extract relevant stats."""
    with open(file, 'r') as f:
        lines = f.readlines()

    stats = {}
    for line in lines:
        if "Elapsed (wall clock) time" in line:
            stats['wall_time'] = re.search(r'(\d+):(\d+):(\d+.\d+)', line).groups()
        if "User time (seconds)" in line:
            stats['cpu_time'] = float(line.split(":")[1].strip())
        if "Maximum resident set size" in line:
            stats['max_memory'] = int(line.split(":")[1].strip())

    return stats

def process_all_results():
    """Process all timing result files and summarize the results."""
    result_files = [f for f in os.listdir() if f.startswith('time_report_')]
    all_results = []

    for file in result_files:
        task_id = re.search(r'time_report_(\d+)\.txt', file).group(1)
        stats = parse_time_report(file)
        all_results.append((task_id, stats))

    # Print out the summary (could also save to a CSV or similar)
    for task_id, stats in all_results:
        print(f"Task {task_id}:")
        print(f"  Wall Time: {stats['wall_time']} (hh:mm:ss)")
        print(f"  CPU Time: {stats['cpu_time']} seconds")
        print(f"  Max Memory: {stats['max_memory']} KB")
        print()

if __name__ == "__main__":
    process_all_results()
