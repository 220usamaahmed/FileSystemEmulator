from src.data_store import DataStore
import config
import os


data_store = None
cwd = "/"
opened_file = None


# def main():
    # To Demo, Comment/Uncomment the functions below
    # data_store = DataStore(config.DATA_STORE)

    # 1. Add a file (single block)
    # data_store.create_file(b"", "/name2.txt")
    
    # 2. Read small file
    # print(data_store.read_file("/name2.txt"))

    # 3. Update a file (multiple blocks)
    # data_store.update_file(b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut leo nec nisl fermentum tristique a sed diam. Phasellus eleifend, mi eu auctor ornare, nulla eros vulputate quam, a viverra metus sem vel enim. Integer egestas, mi et interdum finibus, leo felis bibendum lacus, eget dapibus risus ligula eu velit. In libero.", "/name.txt")
    
    # 4. Read large file
    # print(data_store.read_file("/document1.txt"))

    # 5. Deleting file
    # data_store.delete_file("/name.txt")

    # 6. Create folder
    # data_store.create_folder("/my_documents")
    
    # 7. Create file inside folder
    # data_store.create_file(b"ABCDEF", "/my_documents/name.txt")

    # 8. Read file in folder
    # print(data_store.read_file("/my_documents/name.txt"))

    # 9. Printing index
    # print(data_store.descriptor)


def main():

    global data_store, cwd, opened_file

    os.system("clear")
    data_store = DataStore(config.DATA_STORE)

    COMMANDS = {
        "help": [help, 0],
        "create": [create, 1],
        "delete": [delete, 1],
        "mkdir": [mkdir, 1],
        "chdir": [chdir, 1],
        "move": [move, 2],
        "open-file": [open_file, 1],
        "close-file": [close_file, 0],
        "write-append": [write_append, 1],
        "write-at": [write_at, 2],
        "read": [read, 0],
        "move-within-file": [move_within_file, 3],
        "truncate-file": [truncate_file, 1],
        "show-mem-map": [show_mem_map, 0],
        "exit": [exit, 0]
    }

    while True:
        cli_prompt = f"{cwd}{opened_file} - " if opened_file else f"{cwd} - "
        user_input = input(cli_prompt).split(" ")
        if len(user_input) and user_input[0] in COMMANDS:
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

    COMMANDS["create"][0]()


def help():
    with open("help.txt", 'r') as f:
        print(f.read())


def create(filename):
    data_store.create_file(b"", f"{cwd}{filename}")


def delete(filename):
    data_store.delete_file(f"{cwd}{filename}")


def mkdir(dirname):
    data_store.create_directory(f"{cwd}{dirname}/")


def chdir(dirname):
    global cwd
    # TODO Check if directory exists
    cwd += "dirname/"


def move(source_filename, target_filename):
    data_store.move_file(source_filename, target_filename)


def open_file(filename):
    global opened_file
    # TODO Check if file exists
    opened_file = filename


def close_file():
    global opened_file
    opened_file = None


def write_append(text):
    orig_data = data_store.read_file(f"{cwd}{opened_file}")
    data_store.update_file(orig_data + text.encode(), f"{cwd}{opened_file}")


def write_at(text, at):
    orig_data = data_store.read_file(f"{cwd}{opened_file}").decode()
    data_store.update_file(orig_data[:int(at)] + text.encode(), f"{cwd}{opened_file}")


def read():
    print(data_store.read_file(f"{cwd}{opened_file}").decode())


def move_within_file(start, size, target):
    orig_data = data_store.read_file(f"{cwd}{opened_file}")
    data_to_move = orig_data[int(start):int(start)+int(size)]
    updated_data = orig_data[:int(target)]
    + data_to_move + orig_data[int(target) + int(size):]
    data_store.update_file(updated_data, f"{cwd}{opened_file}")


def truncate_file(max_size):
    orig_data = data_store.read_file(f"{cwd}{opened_file}")
    data_store.update_file(orig_data[:int(max_size)], f"{cwd}{opened_file}")


def show_mem_map():
    print(data_store.descriptor)


def exit():
    os.system("clear")
    quit()


if __name__ == "__main__": main()