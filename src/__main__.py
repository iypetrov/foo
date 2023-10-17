import argparse
from enum import Enum
from src.generation.master_data_api.index import generate_crud_template_master_data_api


class ActionOptions(str, Enum):
    GENERATION = 'generate'


class GenerateOptions(str, Enum):
    MASTER_DATA_API_CRUD_GENERATION = 'm'


def main():
    parser = argparse.ArgumentParser(
        description='This is a python CLI tool designed for automating tasks related to a BPA project.')
    subparsers = parser.add_subparsers(dest='action', title='Available Actions',
                                       description='Choose an action to perform.')

    generation_parser = subparsers.add_parser(ActionOptions.GENERATION,
                                              help='Generate CRUD template for master-data-api')
    generation_parser.add_argument('generate_options', choices=list(GenerateOptions),
                                   help='Generate CRUD template for master-data-api')
    generation_parser.add_argument('model', help='Name of the desired model')

    args = parser.parse_args()

    if args.action == ActionOptions.GENERATION:
        if args.generate_options == GenerateOptions.MASTER_DATA_API_CRUD_GENERATION:
            generate_crud_template_master_data_api(args.model)


if __name__ == '__main__':
    main()
