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


def main():
    root_path = (input('Please input the root path of database: '))

    print()
    print('Start Loading Metadata...')
    buffer = []  # The Buffer for Tables
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                table = Table.load(file)
                buffer.append(table)
    print('Metadata Successfully Loaded!')
    print()

    while __choice_to_function('Select your operation: ',
                               {
                                   'Show Tables': show_tables,
                                   'Enter a Table': enter_table,
                                   'Create a Table': create_table,
                                   'Drop a Table': drop_table,
                                   'Quit': lambda _: False
                               }, buffer, root_path):
        pass


if __name__ == '__main__':
    main()
