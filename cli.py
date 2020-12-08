from src.data_store import DataStore
import config
import os


data_store = None
cwd = []
opened_file = None


def main():
    global data_store, cwd, opened_file

    data_store = DataStore(config.DATA_STORE)
    cwd.append(data_store.root_directory)

    os.system("clear")
    print("\nType help to get help.\n")

    COMMANDS = {
        "help": [help, 0],
        "create": [create, 1],
        "del": [delete, 1],
        "ls": [list_contents, 0],
        "mkdir": [mkdir, 1],
        "cd": [chdir, 1],
        "mv": [move, 2],
        "open": [open_file, 1],
        "close": [close_file, 0],
        "append": [write_append, 0],
        "write": [write_at, 0],
        "read": [read, 0],
        "move-within": [move_within_file, 0],
        "truncate": [truncate_file, 0],
        "show-mem-map": [show_mem_map, 0],
        "clear": [clear, 0],
        "exit": [exit, 0]
    }

    while True:
        cwd_path = "/" + "/".join(list(map(lambda d: d.name, cwd[1:])))
        prompt = f"{cwd_path}/\u001b[32m({opened_file})\u001b[0m> " if opened_file \
        else f"{cwd_path}> "
        user_input = input(prompt).split(" ")
        if user_input[0] == "": continue

        if user_input[0] in COMMANDS:
            command = COMMANDS[user_input[0]]
            if len(user_input[1:]) == command[1]:
                try: command[0](*user_input[1:])
                except Exception as e: print(e)
            else:
                print(f"{user_input[0]} takes {command[1]} arguments, " \
                f"R{len(user_input[1:])} given.")
        else:
            print(f"Command not recognized {user_input[0]}, " \
            "type help for help.")


def help():
    with open("help.txt", 'r') as f:
        print(f.read())


def create(file_name):
    data_store.create_file(cwd[-1], file_name, b"")


def delete(file_name):
    data_store.delete_file(cwd[-1], file_name)


def list_contents():
    print("\t".join([f"\u001b[32m{f}\u001b[0m" for f in cwd[-1].list_files()]
        + [f"\u001b[33m{d}\u001b[0m" for d in cwd[-1].list_sub_directories()]))


def mkdir(directory_name):
    print(data_store.create_directory(cwd[-1], directory_name))


def chdir(directory_name):
    if directory_name == "..":
        if len(cwd) > 1: del cwd[-1]
    elif directory_name == ".": pass
    else:
        cwd.append(data_store.load_directory(cwd[-1], directory_name))


def move(file_name, destination_filepath):
    # Getting destination directory object
    destination_directory = cwd[0]
    for directory_name in destination_filepath.split("/"):
        if destination_directory.sub_directory_exists(directory_name):
            destination_directory = data_store.load_directory(
                destination_directory, directory_name)
        else: raise Exception("The destination folder does not exist.")

    data_store.move_file(cwd[-1], destination_directory, file_name)


def open_file(file_name):
    global opened_file
    opened_file = data_store.load_file(cwd[-1], file_name)


def close_file():
    global opened_file
    opened_file = None


def read():
    if opened_file == None: raise Exception("No open file.")
    print("--- {opened_file.name} START ---")
    print(opened_file.get_data().decode())
    print("--- {opened_file.name} END ---")


def write_append():
    if opened_file == None: raise Exception("No open file.")
    text = input("Enter text:")
    opened_file.append(text.encode())
    data_store.save_updated_file(opened_file)


def write_at():
    if opened_file == None: raise Exception("No open file.")
    text = input("Enter text to write:")
    at = input("Enter position:")
    opened_file.write_at(text.encode(), at)
    data_store.save_updated_file(opened_file)


def move_within_file():
    if opened_file == None: raise Exception("No open file.")
    start = input("Enter start position:")
    size = input("Enter size:")
    at = input("Enter target position:")
    opened_file.move_within(start, size, target)
    data_store.save_updated_file(opened_file)


def truncate_file():
    if opened_file == None: raise Exception("No open file.")
    at = input("Enter position:")
    opened_file.truncate(text.encode(), at)
    data_store.save_updated_file(opened_file)


def show_mem_map():
    print(data_store.block_manager)


def clear():
    os.system("clear")


def exit():
    os.system("clear")
    quit()


if __name__ == "__main__": main()