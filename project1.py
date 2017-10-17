import os
from pathlib import Path
from pathlib import PurePath


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


'''
input_valid = False


def get_directory_list(user_input_path: str) -> list:
    '''Creates a list of files in dir selected and lists all the paths'''
    '''
    if os.path.exists(user_input_path):
        dirc = filter_hidden(user_input_path)
        for file in dirc:
            user_input_path = first_user_input[2:] + "/" + str(file)
            print(pathlib.PurePath(user_input_path))
    '''
    f = Path(user_input_path)
    if f.exists():

        file_list = list(f.iterdir())
        file_list.sort()

        return file_list


    else:
        print("ERROR")
        first_user_input = input()

def get_directory_list_recursive(user_input_path: str) -> list:
    total_file_list = []
    all_files_in_this_dir = get_directory_list(user_input_path)
    for file_path in all_files_in_this_dir:
        f = Path(file_path)
        total_file_list.append(file_path)
        if f.is_dir():

            total_file_list.extend(get_directory_list_recursive(file_path))



    total_file_list.sort()
    return total_file_list



def name_search(file_list, user_input):

    file_name_list = []
    for file_path in file_list:
        if user_input == PurePath(file_path).name:
            file_name_list.append(file_path)

    return file_name_list


def extension_search(file_list, user_input):

    same_extension_list = []
    for file_path in file_list:
        file_suffix = PurePath(file_path).suffix
        if user_input == file_suffix:
            same_extension_list.append(file_path)



    return same_extension_list


def text_search(file_list, user_input):
    same_text_list = []
    for file_path in file_list:
        if str(PurePath(file_path).name).startswith("."):
            continue
        else:
            f = Path(file_path)
            #file_handle = open(file_path, 'r')
            if f.is_file():
                q = f.open('r')
                #file = file_handle.read()

                #print(q.readlines())
                try:

                    x = q.readlines()
                    for line in x:
                        #print(line)
                        line = line.strip()
                        if user_input in line:
                            same_text_list.append(file_path)

                #file_handle.close()
                except Exception as e:
                    '''
                    print(e)
                    print(str(file_path) + " not a text file")
                    '''
                q.close()

    return same_text_list


def less_than_search(file_list, user_input):
    less_than_list = []
    for file_path in file_list:
        p = Path(file_path)
        if user_input > p.stat().st_size:
            less_than_list.append(file_path)

    return less_than_list

def greater_than_search(file_list, user_input):
    greater_than_list = []
    for file_path in file_list:
        p = Path(file_path)
        if user_input < p.stat().st_size:
            greater_than_list.append(file_path)

    return greater_than_list




def narrow_search_commands(file_list):
    narrow_search_input = input()
    narrow_search_input_valid = False
    #while narrow_search_input_valid == False:
    #if narrow_search_input == "A":

    if narrow_search_input[0:2] == "N ":
        for match in name_search(file_list, narrow_search_input[2:]):
            print(match)

    if narrow_search_input[0:2] == "E ":

        for match in extension_search(file_list, narrow_search_input[2:]):
            print(match)


    if narrow_search_input[0:2] == "T ":
        for match in text_search(file_list, narrow_search_input[2:]):
            print(match)


    if narrow_search_input[0:2] == "< ":
        for match in less_than_search(file_list, int(narrow_search_input[2:])):
            print(match)

    if narrow_search_input[0:2] == "> ":
        for match in greater_than_search(file_list, int(narrow_search_input[2:])):
            print(match)



while input_valid == False:
    #List all the files in that directory. No subdirectories

    first_user_input = input()
    if first_user_input[0:2] == "D ":
        for file in get_directory_list(first_user_input[2:]):
                print(file)

        input_valid = True
        narrow_search_commands(get_directory_list(first_user_input[2:]))

    #Recursive so all files until you get the last one
    elif first_user_input[0:2] == "R ":
        '''
        for file in recursion_print_directory(get_directory_list(first_user_input[2:])):
            print(file)
        
        recursion_print_directory(get_directory_list(first_user_input[2:]))
        for file in total_file_list:
            print(file)
        input_valid = True
        #narrow_search_commands(recursion_print_directory(get_directory_list(first_user_input[2:])))
        narrow_search_commands(total_file_list)
        '''
        for file in get_directory_list_recursive(first_user_input[2:]):
            print(file)
    else:
        print("ERROR")

        






