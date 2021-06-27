import PyInquirer
import tabulate
import os

from typing import Callable, Dict, List

from backend import Table, Type


def __choice_to_function(message: str, choices: Dict[str, Callable[[str], bool]], buffer: List[Table]) -> bool:
    return choices[
        PyInquirer.prompt([{
            'type': 'list', 'name': 'op', 'message': message, 'choices': list(choices.keys())
        }])](buffer)


def show_tables(buffer: List[Table]) -> bool:
    return True


def enter_table(buffer: List[Table]) -> bool:
    return True


def create_table(buffer: List[Table]) -> bool:
    return True


def drop_table(buffer: List[Table]) -> bool:
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
                               }, buffer):
        pass


if __name__ == '__main__':
    main()
