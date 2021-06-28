import PyInquirer
import tabulate
import os

from typing import Callable, Dict, List

from backend import Table, Type


def __choice_to_function(message: str, choices: Dict[str, Callable[[str], bool]], buffer: Dict[str, Table],
                         root_path: str) -> bool:
    return choices[
        PyInquirer.prompt([{
            'type': 'list', 'name': 'op', 'message': message, 'choices': list(choices.keys())
        }])['op']](buffer, root_path)


def __choice_to_function2(message: str, choices: Dict[str, Callable[[str], bool]], table: Table,
                          root_path: str) -> bool:
    return choices[
        PyInquirer.prompt([{
            'type': 'list', 'name': 'op', 'message': message, 'choices': list(choices.keys())
        }])['op']](table, root_path)


def exit(buffer: Dict[str, Table], root_path) -> bool:
    print('Bye!')
    print()
    return False


def __not_null(v: str):
    return len(v) != 0


__create_table = [{
    'type': 'input', 'name': 'name', 'message': 'Please Enter a New Table Name:', 'validate': __not_null
}, {
    'type': 'input', 'name': 'desc', 'message': 'Please Describe This Table:', 'validate': __not_null
}]

__enter_table = [{
    'type': 'input', 'name': 'name', 'message': 'Please Enter The Table Name:', 'validate': __not_null
}]

__enter_field = [{
    'type': 'input', 'name': 'name', 'message': 'Please Enter The Field Name:', 'validate': __not_null
}, {
    'type': 'input', 'name': 'desc', 'message': 'Please Describe This Field:', 'validate': __not_null
    # }, {
    #     'type': 'input', 'name': 'type', 'message': 'Please Describe This Table:', 'validate': __not_null
}]

__enter_desc = [{
    'type': 'input', 'name': 'desc', 'message': 'Please Enter The Descption:', 'validate': __not_null
}]


def show_tables(buffer: Dict[str, Table], root_path) -> bool:
    headers = ['TableName', 'Description']
    data = []
    for table in buffer:
        name = table
        desc = buffer[table].desc
        row = [name, desc]
        data.append(row)
    print()
    print(tabulate.tabulate(data, headers, tablefmt='pretty'))
    print()

    return True


def show_table(buffer: Dict[str, Table], root_path) -> bool:
    name = PyInquirer.prompt(__enter_table)['name']
    # print(name)
    __show_table(buffer, name)

    return True


def __show_table(buffer: Dict[str, Table], name: str):
    headers = ['FieldName', 'Description']
    data = []
    table = buffer[name]
    for field in table.fields:
        row = [field.name, field.desc]
        data.append(row)
    print()
    print(tabulate.tabulate(data, headers, tablefmt='pretty'))
    print()


def enter_table(buffer: Dict[str, Table], root_path) -> bool:
    name = PyInquirer.prompt(__enter_table)['name']
    __show_table(buffer, name)
    table = buffer[name]
    while __choice_to_function2('Select Your Option: ', {
        'Add New Field': add_field,
        'Remove Old Field': remove_field,
        'Edit Description': edit_desc,
        'Back': back
    }, table, root_path):
        pass
    return True


def back(table: Table, root_path):
    return False


def add_field(table: Table, root_path) -> bool:

    return True


def remove_field(table: Table, root_path) -> bool:
    return True


def edit_desc(table: Table, root_path) -> bool:
    desc = PyInquirer.prompt(__enter_desc)['desc']
    table.desc = desc
    table.save(table)
    return True


def create_table(buffer: Dict[str, Table], root_path) -> bool:
    info = PyInquirer.prompt(__create_table)
    name = info['name']
    desc = info['desc']
    fields = []
    file = os.path.join(root_path, name + '.json')
    table = Table(file, name, desc, fields)
    table.save(table)
    buffer.setdefault(name, table)
    return True


def drop_table(buffer: Dict[str, Table], root_path) -> bool:
    return True
