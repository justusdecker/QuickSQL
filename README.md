# QuickSQL

![Nah](./demo/header.png)

QSQL is a SQL Template Scripting Language that converts a simple Template to Python-SQLAlchemy compatible code, with Accessor etc.

work in progress

## Features

* Syntax-highlighting for `.sq` files
* The `.sq` to `.py` Converter

## Documentation

Pay attention to the indentation: `root` for table inits and `4 spaces` for columns.

### Table Initialization

`<Table@'table_name'>`

### Columns

`var_name: type`

`var_name: type -> default_val`

### Usage of sqlalchemy classes and functions

`use <module_or_func>`

### Database Declaration

`<Database@'sql_name'>`

### A quick Demo
![Nah](./demo/highlighter.PNG)

will result in:




![Nah](./demo/sheader.png)

Licensed under [MIT](./LICENSE).