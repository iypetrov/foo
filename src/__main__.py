import argparse
from enum import Enum
from src.generation.master_data_api.index import generate_crud_template_master_data_api


class GenerateOptions(str, Enum):
    MASTER_DATA_API_CRUD_GENERATION = 'm'


def main():
    parser = argparse.ArgumentParser(
        description='This is a python CLI tool designed for automating tasks related to a FOO project.')

    parser.add_argument('-generate', '-g', dest='generate_options', choices=list(GenerateOptions))
    parser.add_argument('model')

    args = parser.parse_args()

    if args.generate_options == GenerateOptions.MASTER_DATA_API_CRUD_GENERATION:
        generate_crud_template_master_data_api(args.model)


if __name__ == '__main__':
    main()
