import PyInquirer
import tabulate

from typing import Callable, Dict, List


# import backend


def __choice_to_function(message: str, choices: Dict[str, Callable[[str], bool]], root_path: str) -> bool:
    return choices[
        PyInquirer.prompt([{
            'type': 'list', 'name': 'op', 'message': message, 'choices': list(choices.keys())
        }])](root_path)


def show_tables(root_path: str) -> bool:
    return True


def enter_table(root_path: str) -> bool:
    return True


def create_table(root_path: str) -> bool:
    return True


def drop_table(root_path: str) -> bool:
    return True


def main():
    root_path = (input('Please input the root path of database: '))
    while __choice_to_function('Select your operation: ',
                               {
                                   'Show Tables': show_tables,
                                   'Enter a Table': enter_table,
                                   'Create a Table': create_table,
                                   'Drop a Table': drop_table,
                                   'Quit': lambda _: False
                               }, root_path):
        pass


if __name__ == '__main__':
    main()
