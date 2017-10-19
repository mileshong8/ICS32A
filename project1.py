import os
from pathlib import Path
from pathlib import PurePath
import shutil
import sys

'''
To do list:

Fix D error handling. How to keep prompting when path does not exist?

A get all from previous step
N get all with name (How to get path from file name?)
E fix .pdf vs pdf
T Text in a file
< Done
> Done

AFTER INTERESTING FILES FOUND
F
D
T

check possiblity for errors


'''


def print_list(file_list: list) ->  None:
    '''Prints file paths from list of file paths'''
    if file_list == []:
        sys.exit()

    else:
        for file_path in file_list:
            print(file_path)



def get_directory_list(user_input_path: str, include_dirs: bool) -> list:
    '''Creates a list of files in dir selected and lists all the paths'''
    if include_dirs == False:
        f = Path(user_input_path)
        if f.exists():
            no_dir_list = []
            file_list = list(f.iterdir())
            for file_path in file_list:
                f = Path(file_path)
                if f.is_file():
                    no_dir_list.append(file_path)


            no_dir_list.sort()
            return no_dir_list


        else:
            print("ERROR")
            primary_search()

    else:
        f = Path(user_input_path)
        if f.exists():
            file_list = list(f.iterdir())
            file_list.sort()

            return file_list


        else:
            print("ERROR")
            primary_search()



def get_directory_list_from_all_subdirs(user_input_path: str) -> list:
    '''Takes in a list and finds all paths recursively'''

    total_file_list = []
    total_dir_list = []
    all_files_in_this_dir = get_directory_list(user_input_path, True)
    for file_path in all_files_in_this_dir:
        f = Path(file_path)
        if f.exists():



            if f.is_dir():
                total_dir_list.append(file_path)

            else:
                total_file_list.append(file_path)




        else:
            print("ERROR")
            primary_search()

    total_file_list.sort()
    total_dir_list.sort()

    for dir_path in total_dir_list:
        total_file_list.extend(get_directory_list_from_all_subdirs(dir_path))


    return total_file_list



def from_previous_step(file_list: list) -> list:
    '''Return all the files from the previous step'''
    return file_list


def name_search(file_list: list, user_input: str) -> list:
    '''takes in a list and the user input and returns a list with all files thats name match with the user input'''

    file_name_list = []
    for file_path in file_list:
        if user_input == PurePath(file_path).name:
            file_name_list.append(file_path)

    return file_name_list


def extension_search(file_list: list, user_input: str) -> list:
    '''takes in a list and user input and returns a list with all files thats extension matches with the user input'''
    same_extension_list = []
    for file_path in file_list:
        file_suffix = PurePath(file_path).suffix
        if not user_input.startswith("."):
            user_input = "." + user_input
        if user_input == file_suffix:
            same_extension_list.append(file_path)



    return same_extension_list


def text_search(file_list: list, user_input: str) -> list:
    '''takes in a list and user input and returns a list with all files that have text that matches with the user input'''
    same_text_list = []
    for file_path in file_list:

        if str(PurePath(file_path).name).startswith("."):
            continue
        else:
            f = Path(file_path)
            if f.is_file():
                q = f.open('r')

                try:

                    x = q.readlines()
                    for line in x:

                        line = line.strip().rstrip()
                        if user_input in line:
                            same_text_list.append(file_path)


                except UnicodeDecodeError:
                    pass

                q.close()

    return_same_text_list = []

    for file_path in same_text_list:
        if file_path not in return_same_text_list:
            return_same_text_list.append(file_path)


    return return_same_text_list


def less_than_search(file_list: list, user_input: int) -> list:
    '''takes in a list and user input and returns a list with all files thats size is less than the user input'''
    less_than_list = []
    for file_path in file_list:
        p = Path(file_path)
        if user_input > p.stat().st_size:
            less_than_list.append(file_path)

    return less_than_list

def greater_than_search(file_list: list, user_input: int) -> list:
    '''takes in a list and user input and returns a list with all files thats size is greater than the user input'''
    greater_than_list = []
    for file_path in file_list:
        p = Path(file_path)
        if user_input < p.stat().st_size:
            greater_than_list.append(file_path)

    return greater_than_list

def print_first_line_of_text_file(file_list) -> list:
    return_first_lines = []
    first_lines = []
    for file_path in file_list:
        f = Path(file_path)
        if f.is_file():
            q = f.open('r')

            try:

                x = q.readlines()

                first_lines.append(x[0])

            except UnicodeDecodeError:
                pass

            q.close()

    for first_line in first_lines:
        return_first_lines.append(first_line.rstrip())

    return return_first_lines

def copy_files(file_list: list) -> None:
    for file_path in file_list:
        f = Path(file_path)
        if f.is_file():
            shutil.copy(str(file_path), (str(file_path) + ".dup"))

def touch_file(file_list: list) -> None:
    for file_path in file_list:
        f = Path(file_path)
        f.touch()


def actions_commands(file_list: list) -> None:
    actions_input = input()
    if actions_input == "F":
        if print_first_line_of_text_file(file_list) == []:
            print("NO TEXT")

        else:
            for line in print_first_line_of_text_file(file_list):
                print(line)

            sys.exit()

    if actions_input == "D":
        copy_files(file_list)
        sys.exit()

    if actions_input == "T":
        touch_file(file_list)
        sys.exit()

    else:
        print("ERROR")
        actions_commands(file_list)







def narrow_search_commands(file_list: list) -> None:
    narrow_search_input = input()
    narrow_search_input_valid = False
    #while narrow_search_input_valid == False:
    if narrow_search_input == "A":
        print_list(from_previous_step(file_list))

        actions_commands(from_previous_step(file_list))

    elif narrow_search_input[0:2] == "N ":
        print_list(name_search(file_list, narrow_search_input[2:]))


        actions_commands(name_search(file_list, narrow_search_input[2:]))

    elif narrow_search_input[0:2] == "E ":
        print_list(extension_search(file_list, narrow_search_input[2:]))

        actions_commands(extension_search(file_list, narrow_search_input[2:]))


    elif narrow_search_input[0:2] == "T ":
        print_list(text_search(file_list, narrow_search_input[2:]))

        actions_commands(text_search(file_list, narrow_search_input[2:]))


    elif narrow_search_input[0:2] == "< ":
        print_list(less_than_search(file_list, int(narrow_search_input[2:])))

        actions_commands(less_than_search(file_list, int(narrow_search_input[2:])))

    elif narrow_search_input[0:2] == "> ":
        print_list(greater_than_search(file_list, int(narrow_search_input[2:])))

        actions_commands(greater_than_search(file_list, int(narrow_search_input[2:])))

    else:
        print("ERROR")
        narrow_search_commands(file_list)

def primary_search():
    input_valid = False
    first_user_input = input()
    while input_valid == False:
        # List all the files in that directory. No subdirectories


        if first_user_input[0:2] == "D ":

            print_list(get_directory_list(first_user_input[2:], False))

            input_valid = True
            narrow_search_commands(get_directory_list(first_user_input[2:], False))

        # Recursive so all files until you get the last one
        elif first_user_input[0:2] == "R ":

            print_list(get_directory_list_from_all_subdirs(first_user_input[2:]))

            input_valid = True
            narrow_search_commands(get_directory_list_from_all_subdirs(first_user_input[2:]))
        else:
            print("ERROR")
            primary_search()


primary_search()




