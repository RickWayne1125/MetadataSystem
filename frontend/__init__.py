import PyInquirer
import tabulate
import os

from typing import Callable, Dict, List

from backend import Table, Type


def __choice_to_function(message: str, choices: Dict[str, Callable[[str], bool]], buffer: List[Table],
                         root_path: str) -> bool:
    return choices[
        PyInquirer.prompt([{
            'type': 'list', 'name': 'op', 'message': message, 'choices': list(choices.keys())
        }])['op']](buffer, root_path)


def exit(buffer: List[Table], root_path) -> bool:
    print('Bye!')
    return False


def __not_null(v: str):
    return len(v) != 0


__create_table = [{
    'type': 'input', 'name': 'name', 'message': 'Please Enter a New Table Name:', 'validate': __not_null
}, {
    'type': 'input', 'name': 'desc', 'message': 'Please Describe This Table:', 'validate': __not_null
}]


def show_tables(buffer: List[Table], root_path) -> bool:
    headers = ['TableName', 'Description']
    data = []
    for table in buffer:
        name = table.name
        desc = table.desc
        row = [name, desc]
        data.append(row)
    print()
    print(tabulate.tabulate(data, headers, tablefmt='pretty'))
    print()

    return True


def enter_table(buffer: List[Table], root_path) -> bool:
    return True


def create_table(buffer: List[Table], root_path) -> bool:
    info = PyInquirer.prompt(__create_table)
    name = info['name']
    desc = info['desc']
    fields = []
    file = os.path.join(root_path, name + '.json')
    table = Table(file, name, desc, fields)
    table.save(table)
    buffer.append(table)
    return True


def drop_table(buffer: List[Table], root_path) -> bool:
    return True
