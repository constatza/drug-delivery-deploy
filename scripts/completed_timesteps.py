from pathlib import Path
import argparse
import sys


def main(args=None):
    """
    This script reads the timeStepTotalTimes*.txt file in each subdirectory of the results_root directory and
    calculates the fraction of completed timesteps. It then writes the results to a csv file.
    """
    if args is None:
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description='Extrapolate required time for Bio analysis')
    parser.add_argument('results_root', type=Path, help='Root directory for results')
    parser.add_argument('--filename', type=str, help='Name of the file to seek in each subdirectory',
                        default='timeStepTotalTimes.txt')
    parser.add_argument('--output', '-o', type=Path, help='Output file path',
                        default=None)

    args = parser.parse_args(args)
    results_root = args.results_root
    file_to_seek = args.filename
    output_path = args.output

    if not results_root.is_dir():
        raise FileNotFoundError(f"Directory {results_root} not found")

    if output_path is None:
        output_path = results_root

    if results_root.is_dir():
        # get all subdirs with format %x_%a
        subdirs = [x for x in results_root.iterdir() if x.is_dir() if x.name.split('_')[-1].isdigit()]
        idxs = tuple(map(lambda x: int(x.name.split('_')[-1]), subdirs))
        sorted_dirs_by_idx = sorted(zip(idxs, subdirs))
        idxs, subdirs = zip(*sorted_dirs_by_idx)
        files = tuple(map(lambda x: x / file_to_seek, subdirs))

        floats = tuple(map(read_results, files))
        nonzero = tuple(map(count_nonzero, floats))
        total_timesteps = tuple(map(lambda x: len(x), floats))
        completed_fraction = tuple(map(lambda x, y: x/y, nonzero, total_timesteps))
        write_csv(output_path, nonzero, total_timesteps, completed_fraction)
        print("Done")


def write_csv(path, completed_timesteps, total_timesteps, fraction):
    filename = path / f'completed_timesteps.csv'
    header = "Completed Timesteps, Completed Fraction, Total Timesteps\n"
    with open(filename, "w") as f:
        f.write(header)
        for i in range(len(completed_timesteps)):
            f.write(f"{completed_timesteps[i]:d}, {fraction[i]:.5e}, {total_timesteps[i]:d}\n")


def read_results(results_file: Path) -> tuple:
    with open(results_file, 'r') as f:
        # read only one line
        line = f.readline()
        # split the line into a list of strings then convert each string to a float
        numbers = tuple(float(x) for x in line.split())
    return numbers


def count_nonzero(times: tuple) -> int:
    # count the nonzeros as percentage of the total length
    return sum([1 for x in times if x != 0])


if __name__ == "__main__":
    main()
