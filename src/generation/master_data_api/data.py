from enum import Enum
from src.config.index import USERNAME, MASTER_DATA_API_DIR
from src.generation.util import convert_model_to_snake_case, convert_word_to_one_starting_with_lower_case, convert_model_to_kebab_case, \
    convert_model_to_de_sentence, convert_model_to_en_sentence

JAVA_EXTENSION = '.java'
PROPERTIES_EXTENSION = '.properties'
XML_EXTENSION = '.xml'
CHANGELOG_MASTER_FILE = f'db.changelog-master{XML_EXTENSION}'

MASTER_DATA_DIR = f'/src/main/java/com/iteconomics/bpa/masterdata'
TEST_MASTER_DATA_DIR = f'/src/test/java/com/iteconomics/bpa/masterdata/controllers'
MESSAGES_DIR = f'/src/main/resources'
DB_CHANGELOG_DIR = f'/src/main/resources/db/changelog'


class TargetTypeEnum(str, Enum):
    ENTITY = 'Entity'
    REPOSITORY = 'Repository'
    SERVICE = 'Service'
    CONTROLLER = 'Controller'
    DTO = 'DTO'
    TEST_CONTROLLER = 'ControllerTest'


class TargetDirEnum(str, Enum):
    ENTITIES_DIR = 'entities'
    REPOSITORIES_DIR = 'repositories'
    SERVICES_DIR = 'services'
    CONTROLLERS_DIR = 'controllers'
    DTOS_DIR = 'dtos'
    TEST_CONTROLLERS_DIR = 'ControllerTest'


target_enum_to_dir_mapping = {
    TargetTypeEnum.ENTITY: TargetDirEnum.ENTITIES_DIR.value,
    TargetTypeEnum.REPOSITORY: TargetDirEnum.REPOSITORIES_DIR.value,
    TargetTypeEnum.SERVICE: TargetDirEnum.SERVICES_DIR.value,
    TargetTypeEnum.CONTROLLER: TargetDirEnum.CONTROLLERS_DIR.value,
    TargetTypeEnum.DTO: TargetDirEnum.DTOS_DIR.value,
    TargetTypeEnum.TEST_CONTROLLER: TargetDirEnum.TEST_CONTROLLERS_DIR.value,
}


def create_java_file(target, model):
    return f'{MASTER_DATA_API_DIR}{MASTER_DATA_DIR}/{target_enum_to_dir_mapping[target]}/{model}{target.value}{JAVA_EXTENSION}'


def create_test_controller_file(target, model):
    return f'{MASTER_DATA_API_DIR}{TEST_MASTER_DATA_DIR}/{model}{target.value}{JAVA_EXTENSION}'


def get_file_message_en():
    return f'{MASTER_DATA_API_DIR}{MESSAGES_DIR}/messages_en{PROPERTIES_EXTENSION}'


def get_file_message_de():
    return f'{MASTER_DATA_API_DIR}{MESSAGES_DIR}/messages_de{PROPERTIES_EXTENSION}'


def get_file_db_changeset(model):
    file_changeset = convert_model_to_kebab_case(model)
    return f'{MASTER_DATA_API_DIR}{DB_CHANGELOG_DIR}/changeSet-add-{file_changeset}{XML_EXTENSION}'


def get_file_db_changeset_master():
    return f'{MASTER_DATA_API_DIR}{DB_CHANGELOG_DIR}/{CHANGELOG_MASTER_FILE}'


def get_content_db_changeset_master(model):
    file = get_file_db_changeset(model).split('/')[-1]

    return f'''\t<include file="db/changelog/{file}"/>\n'''


def get_content_message_en(model):
    key = f'{convert_model_to_snake_case(model)}.001'
    return f'''{key}={convert_model_to_en_sentence(model)} not found\n'''


def get_content_message_de(model):
    key = f'{convert_model_to_snake_case(model)}.001'
    return f'''{key}={convert_model_to_de_sentence(model)} nicht vorhanden\n'''


def get_content_entity(model):
    table_name = convert_model_to_snake_case(model)
    return f'''package com.iteconomics.bpa.masterdata.entities;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Entity
@Table(name = "{table_name}")
public class {model} extends BaseEntity {{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name="ID")
    private Long id;
}}
'''


def get_content_repository(model):
    return f'''package com.iteconomics.bpa.masterdata.repositories;

import com.iteconomics.bpa.masterdata.entities.{model};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface {model}Repository extends JpaRepository<{model}, Long> {{
}}
'''


def get_content_service_interface(model):
    arg = convert_word_to_one_starting_with_lower_case(model)
    return f'''package com.iteconomics.bpa.masterdata.services;

import com.iteconomics.bpa.masterdata.dtos.{model}DTO;

import java.util.List;

public interface {model}Service {{
    {model}DTO create{model}({model}DTO {arg}DTO);

    {model}DTO get{model}ById(Long id);

    List<{model}DTO> getAll{model}s();

    {model}DTO update{model}({model}DTO {arg}DTO);

    void delete{model}ById(Long id);
}}
'''


def get_content_service_implementation(model):
    arg = convert_word_to_one_starting_with_lower_case(model)
    msg = convert_model_to_snake_case(model)

    return f'''package com.iteconomics.bpa.masterdata.services;

import com.iteconomics.bpa.masterdata.dtos.{model}DTO;
import com.iteconomics.bpa.masterdata.entities.{model};
import com.iteconomics.bpa.masterdata.repositories.{model}Repository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@AllArgsConstructor
public class {model}ServiceImpl extends BaseService implements {model}Service {{

    private {model}Repository {arg}Repository;

    @Override
    public {model}DTO create{model}({model}DTO {arg}DTO) {{
        {model} {arg} = map({arg}DTO, {model}.class);
        return map({arg}Repository.save({arg}), {model}DTO.class);
    }}

    @Override
    public {model}DTO get{model}ById(Long id) {{
        {model} {arg} = {arg}Repository.findById(id)
                    .orElseThrow(notFound("{model} id: " + id, "{msg}.001"));
        return map({arg}, {model}DTO.class);
    }}

    @Override
    public List<{model}DTO> getAll{model}s() {{
        return map({arg}Repository.findAll(), {model}DTO.class);
    }}

    @Override
    public {model}DTO update{model}({model}DTO {arg}DTO) {{
        if (!{arg}Repository.existsById({arg}DTO.getId())) {{
            throw notFound("{model} id: " + {arg}DTO.getId(), "{msg}.001").get();
        }}
        {model} {arg} = map({arg}DTO, {model}.class);
        return map({arg}Repository.save({arg}), {model}DTO.class);
    }}

    @Override
    public void delete{model}ById(Long id) {{
        {arg}Repository.deleteById(id);
    }}
}}
'''


def get_content_controller(model):
    arg = convert_word_to_one_starting_with_lower_case(model)
    endpoint = convert_model_to_kebab_case(model)
    return f'''package com.iteconomics.bpa.masterdata.controllers;

import com.iteconomics.bpa.masterdata.annotations.SecuredDeleteMapping;
import com.iteconomics.bpa.masterdata.annotations.SecuredGetMapping;
import com.iteconomics.bpa.masterdata.annotations.SecuredPostMapping;
import com.iteconomics.bpa.masterdata.annotations.SecuredPutMapping;
import com.iteconomics.bpa.masterdata.dtos.{model}DTO;
import com.iteconomics.bpa.masterdata.services.{model}Service;
import lombok.AllArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/{endpoint}s")
@AllArgsConstructor
public class {model}Controller extends BaseController {{

    private {model}Service {arg}Service;

    @SecuredPostMapping
    public ResponseEntity<{model}DTO> create{model}(@RequestBody {model}DTO {arg}DTO) {{
        return ResponseEntity.status(HttpStatus.CREATED).body({arg}Service.create{model}({arg}DTO));
    }}

    @SecuredGetMapping("/{{id}}")
    public ResponseEntity<{model}DTO> get{model}ById(@PathVariable Long id) {{
        return ResponseEntity.ok().body({arg}Service.get{model}ById(id));
    }}

    @SecuredGetMapping
    public ResponseEntity<List<{model}DTO>> getAll{model}s() {{
        return ResponseEntity.ok().body({arg}Service.getAll{model}s());
    }}

    @SecuredPutMapping
    public ResponseEntity<{model}DTO> update{model}(@RequestBody {model}DTO {arg}DTO) {{
        return ResponseEntity.ok().body({arg}Service.update{model}({arg}DTO));
    }}

    @SecuredDeleteMapping("/{{id}}")
    public ResponseEntity<Void> delete{model}(@PathVariable Long id) {{
        {arg}Service.delete{model}ById(id);
        return ResponseEntity.noContent().build();
    }}
}}
'''


def get_content_dto(model):
    return f'''package com.iteconomics.bpa.masterdata.dtos;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class {model}DTO {{
    private Long id;
}}
'''


def get_content_test_controller(model):
    arg = convert_word_to_one_starting_with_lower_case(model)
    endpoint = convert_model_to_kebab_case(model)
    const_prefix = convert_model_to_snake_case(model)
    return f'''package com.iteconomics.bpa.masterdata.controllers;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.iteconomics.bpa.masterdata.dtos.{model}DTO;
import com.iteconomics.bpa.masterdata.services.{model}Service;
import org.hamcrest.Matchers;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders;
import org.springframework.test.web.servlet.result.MockMvcResultMatchers;
import org.springframework.test.web.servlet.setup.MockMvcBuilders;

import java.util.List;

@ExtendWith(MockitoExtension.class)
class {model}ControllerTest {{

    private static final long {const_prefix}_ID = 1L;
    private static final String {const_prefix}_ENDPOINT = "/{endpoint}s";

    @Mock
    private {model}Service {arg}Service;
    @InjectMocks
    private {model}Controller {arg}Controller;
    private MockMvc mockMvc;
    {model}DTO {arg}DTO;

    @BeforeEach
    public void setUp() {{
        mockMvc = MockMvcBuilders.standaloneSetup({arg}Controller).build();
        {arg}DTO = create{model}();
    }}

    @Test
    void testCreate{model}() throws Exception {{
        Mockito.when({arg}Service.create{model}(Mockito.any({model}DTO.class)))
                .thenReturn({arg}DTO);

        mockMvc.perform(MockMvcRequestBuilders.post({const_prefix}_ENDPOINT)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(new ObjectMapper().writeValueAsString({arg}DTO)))
                .andExpect(MockMvcResultMatchers.status().isCreated())
                .andExpect(MockMvcResultMatchers.jsonPath("$.id").value({arg}DTO.getId()));
    }}

    @Test
    void testGet{model}ById() throws Exception {{
        Mockito.when({arg}Service.get{model}ById({const_prefix}_ID)).thenReturn({arg}DTO);

        mockMvc.perform(MockMvcRequestBuilders.get({const_prefix}_ENDPOINT + "/{{id}}", {const_prefix}_ID))
                .andExpect(MockMvcResultMatchers.status().isOk());
    }}
    
    @Test
    void testGetAll{model}s() throws Exception {{
        List<{model}DTO> {arg}DTOs = List.of({arg}DTO);

        Mockito.when({arg}Service.getAll{model}s()).thenReturn({arg}DTOs);

        mockMvc.perform(MockMvcRequestBuilders.get({const_prefix}_ENDPOINT))
                .andExpect(MockMvcResultMatchers.status().isOk())
                .andExpect(MockMvcResultMatchers.jsonPath("$", Matchers.hasSize(1)))
                .andExpect(MockMvcResultMatchers.jsonPath("$[0].id", Matchers.is(this.{arg}DTO.getId()), Long.class));
    }}

    @Test
    void testUpdate{model}() throws Exception {{
        Mockito.when({arg}Service.update{model}(Mockito.any({model}DTO.class))).thenReturn({arg}DTO);

        mockMvc.perform(MockMvcRequestBuilders.put({const_prefix}_ENDPOINT)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(new ObjectMapper().writeValueAsString({arg}DTO)))
                .andExpect(MockMvcResultMatchers.status().isOk());
    }}

    @Test
    void testDelete{model}ById() throws Exception {{
        mockMvc.perform(MockMvcRequestBuilders.delete({const_prefix}_ENDPOINT + "/{{id}}", {const_prefix}_ID))
                .andExpect(MockMvcResultMatchers.status().isNoContent());
        Mockito.verify({arg}Service, Mockito.times(1)).delete{model}ById({const_prefix}_ID);
    }}

    private static {model}DTO create{model}() {{
        final {model}DTO {arg} = new {model}DTO();
        {arg}.setId({const_prefix}_ID);
        return {arg};
    }}
}}
'''


def get_content_db_changeset(model, unique_id):
    table_name = convert_model_to_snake_case(model)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<databaseChangeLog xmlns="http://www.liquibase.org/xml/ns/dbchangelog"
                   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                   xsi:schemaLocation="http://www.liquibase.org/xml/ns/dbchangelog
                   https://www.liquibase.org/xml/ns/dbchangelog/dbchangelog-latest.xsd">

    <changeSet author="{USERNAME}" id="{unique_id}">
        <createTable tableName="{table_name}-1">
            <column autoIncrement="true" name="ID" type="BIGINT">
                <constraints nullable="false" primaryKey="true" primaryKeyName="{table_name}_pkey"/>
            </column>

            <column name="CREATED_AT" type="timestamp"/>
            <column name="UPDATED_AT" type="timestamp"/>
        </createTable>
    </changeSet>

</databaseChangeLog>
'''
