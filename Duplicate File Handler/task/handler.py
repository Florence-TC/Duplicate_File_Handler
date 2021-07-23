import os
import sys
import hashlib

args = sys.argv

if len(args) == 1:
    print("Directory is not specified")
else:
    print("Enter file format:")
    file_format = input()

    print('''Size sorting options:
1. Descending
2. Ascending

Enter a sorting option:''')
    sorting_option = int(input())
    while sorting_option not in [1, 2]:
        print("Wrong option")
        sorting_option = int(input())

    output_dict = {}
    sorted_dict = {}

    for root, dirs, files in os.walk(args[1]):
        for name in files:
            file_path = os.path.join(root, name)
            if file_format == "":
                file_size = os.path.getsize(file_path)
                if file_size not in output_dict:
                    output_dict[file_size] = [file_path]
                else:
                    output_dict[file_size].append(file_path)
            elif os.path.splitext(file_path)[1] == f".{file_format}":
                file_size = os.path.getsize(file_path)
                if file_size not in output_dict:
                    output_dict[file_size] = [file_path]
                else:
                    output_dict[file_size].append(file_path)

    if sorting_option == 1:
        sorted_dict = sorted(output_dict, reverse=True)
    elif sorting_option == 2:
        sorted_dict = sorted(output_dict)

    for size in sorted_dict:
        print(f"{size} bytes")
        for file in output_dict[size]:
            print(file)

    print("Check for duplicates?")
    user_answer = input()
    while user_answer not in ["yes", "no"]:
        print("Wrong option")
        user_answer = input()
    else:
        if user_answer == "no":
            pass
        else:
            i = 1
            file_dict = {}
            for size in sorted_dict:
                hash_dict = {}
                for file in output_dict[size]:
                    with open(file, "rb") as the_file:
                        file_hash = hashlib.md5()
                        file_hash.update(the_file.read())
                        file_hash_hex = file_hash.hexdigest()
                        if file_hash_hex not in hash_dict:
                            hash_dict[file_hash_hex] = [file]
                        else:
                            hash_dict[file_hash_hex].append(file)
                lengths = [len(hash_dict[file_hash_hex]) for file_hash_hex in hash_dict]
                if max(lengths) > 1:
                    print(f"{size} bytes")
                for file_hash_hex in hash_dict:
                    if len(hash_dict[file_hash_hex]) > 1:
                        print(f"Hash: {file_hash_hex}")
                        for file in hash_dict[file_hash_hex]:
                            print(f"{i}. {file}")
                            file_dict[i] = file
                            i += 1

    print("Delete files?")
    user_answer = input()
    while user_answer not in ["yes", "no"]:
        print("Wrong option")
        user_answer = input()
    else:
        if user_answer == "no":
            pass
        else:
            print("Enter file numbers to delete:")
            try:
                list_of_files = [int(n) for n in input().split()]
            except ValueError:
                print("Wrong format")
                print("Enter file numbers to delete:")
                list_of_files = [int(n) for n in input().split()]

            if not list_of_files:
                print("Wrong format")
                print("Enter file numbers to delete:")
                list_of_files = [int(n) for n in input().split()]
            elif max(list_of_files) not in file_dict.keys():
                print("Wrong format")
                print("Enter file numbers to delete:")
                list_of_files = [int(n) for n in input().split()]
            else:
                total_size = 0
                for n in list_of_files:
                    total_size += os.path.getsize(file_dict[n])
                    os.remove(file_dict[n])
                print(f"Total freed up space: {total_size} bytes")
