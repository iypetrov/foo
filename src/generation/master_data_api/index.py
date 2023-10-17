import os
from src.generation.master_data_api.data import *
from src.generation.util import create_unique_id, get_num_lines_in_file, get_line_in_message_file_based_on_model


def generate_crud_template_master_data_api(model):
    generate_entity(model)
    generate_repository(model)
    generate_service(model)
    generate_controller(model)
    generate_dto(model)
    generate_test_controller(model)
    update_db_changeset(model)
    update_messages(model)


def generate_entity(model):
    file = create_java_file(TargetTypeEnum.ENTITY, model)
    extension = file[-5:]
    file = file[:-11]
    file = f'{file}{extension}'
    generate_data(file, get_content_entity(model))


def generate_repository(model):
    file = create_java_file(TargetTypeEnum.REPOSITORY, model)
    generate_data(file, get_content_repository(model))


def generate_service(model):
    file = create_java_file(TargetTypeEnum.SERVICE, model)
    generate_data(file, get_content_service_interface(model))

    extension = file[-5:]
    file = file[:-5]
    file = f'{file}Impl{extension}'
    generate_data(file, get_content_service_implementation(model))


def generate_controller(model):
    file = create_java_file(TargetTypeEnum.CONTROLLER, model)
    generate_data(file, get_content_controller(model))


def generate_dto(model):
    file = create_java_file(TargetTypeEnum.DTO, model)
    generate_data(file, get_content_dto(model))


def generate_test_controller(model):
    file = create_test_controller_file(TargetTypeEnum.TEST_CONTROLLER, model)
    generate_data(file, get_content_test_controller(model))


def update_db_changeset(model):
    unique_id = create_unique_id()

    file = get_file_db_changeset(model)
    generate_data(file, get_content_db_changeset(model, unique_id))

    file_master = get_file_db_changeset_master()
    count_lines = get_num_lines_in_file(file_master)
    insert_at_line(file_master, get_content_db_changeset_master(model), count_lines)


def update_messages(model):
    file_en = get_file_message_en()
    line_en = get_line_in_message_file_based_on_model(model, file_en)
    insert_at_line(file_en, get_content_message_en(model), line_en)

    file_de = get_file_message_de()
    line_de = get_line_in_message_file_based_on_model(model, file_de)
    insert_at_line(file_de, get_content_message_de(model), line_de)


def generate_data(file, data):
    try:
        if os.path.exists(file):
            print(f'skipping {file} - already exists')
            return

        with open(file, 'w') as f:
            f.write(data)

        print(f'generation of {file} ended successfully')
    except Exception as ex:
        print(f'error generating {file}: {str(ex)}')


def insert_at_line(file, data, line):
    try:
        with open(file, 'r') as f:
            lines = f.readlines()

        if not lines:
            with open(file, 'w') as f:
                f.write(data)
            print(f'inserted data into {file} (file was empty)')
            return

        if line > len(lines):
            with open(file, 'a') as f:
                f.write(data)
            print(f'appended data to {file} (line number greater than max lines)')
            return

        lines.insert(line - 1, data)

        with open(file, 'w') as f:
            f.writelines(lines)

        print(f'inserted data into {file} at line {line}')
    except Exception as ex:
        print(f'error inserting data into {file}: {str(ex)}')
