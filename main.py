import os
from backend import *
import frontend as fe
import PyInquirer


def main():
    db_dir = 'database'

    op = PyInquirer.prompt([{
        'type': 'list', 'name': 'op', 'message': 'Select Your Operation',
        'choices': ['Enter a Database', 'Create a Database', 'Exit']
    }])['op']

    if op == 'Enter a Database':
        databases = []
        for root, dirs, files in os.walk(db_dir):
            for dir in dirs:
                databases.append(dir)
        root_path = os.path.join(db_dir,
                                 PyInquirer.prompt([{
                                     'type': 'list', 'name': 'op', 'message': 'Select a Database',
                                     'choices': databases
                                 }])['op'])
    elif op == 'Create a Database':
        db_name = input('Enter The New Database Name: ')
        root_path = os.path.join(db_dir, db_name)
        os.mkdir(root_path)
    else:
        fe.exit()

    print()
    print('Start Loading Metadata...')
    buffer = {}  # The Buffer for Tables
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if os.path.splitext(file)[1] == '.json':
                name = os.path.splitext(file)[0]
                table = Table.load(os.path.join(root_path, file))
                buffer.setdefault(name, table)
    print('Metadata Successfully Loaded!')
    print(len(buffer), ' Tables Are Loaded in Total.')
    print()

    while fe.__choice_to_function('Select Your Operation: ',
                                  {
                                      'Show Tables': fe.show_tables,
                                      'Show a Table': fe.show_table,
                                      'Enter a Table': fe.enter_table,
                                      'Create a Table': fe.create_table,
                                      'Drop a Table': fe.drop_table,
                                      'Quit': fe.exit
                                  }, buffer, root_path):
        pass


if __name__ == '__main__':
    main()
