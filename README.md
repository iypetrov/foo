# FOO Dev Tools

## DESCRIPTION

The FOO CLI is a versatile utility designed to streamline various automation tasks associated with a FOO project. It currently supports:
- CRUD template generation for a `master-data-api` component in Java & Spring Boot & Hibernate & Liquibase project


## Configuration

Before using the FOO CLI, you need to set up your environment by creating a .env file in the root directory of your project. This file should contain essential configuration variables required for the tool to function correctly.

Example .env content:
```
USERNAME=ipetrov
MASTER_DATA_API_DIR=/mnt/c/Users/ipetrov/stuff/work/projects/besudb/master-data-api
```

The next step is to go to the root directory and build the project. To do so type:

`$ pip install .`


## OPTIONS

To see all the available options type:

`$ foo -h`


## EXAMPLES

- To generate a CRUD template for a model named "Product":

  `$  foo -generate m Product`
  
   or

  `$  foo -g m Product`

## RUN UNIT TESTS

To run all the unit tests of the FOO CLI itself, go in the root dir and run:

`$  python -m unittest discover -s ./src/tests`
