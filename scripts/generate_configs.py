import random
import xml.etree.ElementTree as et
from pathlib import Path

import yaml


def load_distributions_config(yaml_file):
    """
    Load the parameter ranges from a YAML file.

    Args:
        yaml_file (Path): Path to the YAML file containing parameter ranges.

    Returns:
        dict: A dictionary with parameter ranges.
    """
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)


def sample_param(param_info):
    """
    Sample a parameter value based on its distribution type and parameters.

    Args:
        param_info (dict): A dictionary containing the distribution type and parameters.

    Returns:
        str: A sampled parameter value as a string.
    """
    dist_type = param_info['distribution']
    params = param_info['params']

    # Dynamically import the appropriate random function
    dist_func = getattr(random, dist_type)

    return str(dist_func(*params))


def sample_params(ranges):
    """
    Sample values for all parameters based on their distribution types and parameters.

    Args:
        ranges (dict): A dictionary containing parameter ranges.

    Returns:
        dict: A dictionary with sampled parameter values.
    """
    return {param: sample_param(info) for param, info in ranges.items()}


def update_parameters(input_file, output_file, new_params):
    """
    Update the parameters in the XML configuration file with new sampled values.

    Args:
        input_file (Path): Path to the input XML configuration template.
        output_file (Path): Path to the output XML configuration file.
        new_params (dict): A dictionary with new parameter values.
    """
    tree = et.parse(input_file)
    root = tree.getroot()

    parameters = root.find('Parameters')
    if parameters is not None:
        for param, value in new_params.items():
            element = parameters.find(param)
            if element is not None:
                element.text = str(value)
            else:
                new_element = et.SubElement(parameters, param)
                new_element.text = str(value)

    tree.write(output_file)


def prepare_config_dir(input_file):
    """
    Prepare the directory for storing generated configuration files.

    Args:
        input_file (Path): Path to the input XML configuration template.

    Returns:
        Path: Path to the directory for storing generated configuration files.
    """
    config_dir = input_file.parent.parent / Path("config-auto-generated")
    if config_dir.exists():
        for child in config_dir.iterdir():
            if child.is_file():
                child.unlink()
    else:
        config_dir.mkdir(exist_ok=True, parents=True)
    return config_dir


def generate_configs(template_file, stochastic_params):
    """
    Generate multiple configuration files with random parameters.

    Args:
        template_file (Path): Path to the input XML configuration template.
        stochastic_params (dict): A dictionary with parameter ranges.
    """
    config_dir = prepare_config_dir(template_file)
    num_samples = int(stochastic_params.pop('num_samples'))
    # num_of_digits = len(str(num_of_samples))
    for i in range(num_samples):
        new_params = sample_params(stochastic_params)
        new_name = f"{template_file.stem}_{i:d}{template_file.suffix}"
        output_file = config_dir / new_name
        update_parameters(template_file, output_file, new_params)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate configuration files with random parameters')
    parser.add_argument('distribution', type=Path, help='YAML file with parameter ranges')
    parser.add_argument('--template', type=Path, help='Input configuration template',
                        default='../config/5EquationsSmall.xml')

    args = parser.parse_args()

    distributions_parameters = load_distributions_config(args.distribution)

    generate_configs(args.template, distributions_parameters)


if __name__ == "__main__":
    main()
