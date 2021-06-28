import os
from backend import *
import frontend as fe


def main():
    root_path = (input('Please input the root path of database: '))

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

    while fe.__choice_to_function('Select your operation: ',
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
