from src.data_store import DataStore
import config
import os


data_store = None
cwd = "/"
open_file = None


# def main():
    # To Demo, Comment/Uncomment the functions below
    # data_store = DataStore(config.DATA_STORE)

    # 1. Add a file (single block)
    # data_store.create_file(b"Lorem ipsum dolor sit amet", "/name.txt")
    
    # 2. Read small file
    # print(data_store.read_file("/name.txt"))

    # 3. Update a file (multiple blocks)
    # data_store.update_file(b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ut leo nec nisl fermentum tristique a sed diam. Phasellus eleifend, mi eu auctor ornare, nulla eros vulputate quam, a viverra metus sem vel enim. Integer egestas, mi et interdum finibus, leo felis bibendum lacus, eget dapibus risus ligula eu velit. In libero.", "/name.txt")
    
    # 4. Read large file
    # print(data_store.read_file("/name.txt"))

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
    os.system("clear")
    data_store = DataStore(config.DATA_STORE)

    COMMANDS = {
        "help": [help, 0],
        "create": [create, 1],
        "delete": [delete, 1],
        "mkdir": [mkdir, 1],
        "chdir": [chdir, 1],
        "move": [move, 2],
        "open_file": [open_file, 1],
        "close_file": [close_file, 0],
        "write": [write, 1],
        "read": [read, 0],
        "move_within_file": [move_within_file, 3],
        "truncate_file": [truncate_file, 1],
        "show_mem_map": [show_mem_map, 0],
        "exit": [exit, 0]
    }

    while True:
        user_input = input(f"{cwd} - ").split(" ")
        if len(user_input) and user_input[0] in COMMANDS:
            command = COMMANDS[user_input[0]]
            if len(user_input[1:]) == command[1]:
                try: command[0](*user_input[1:])
                except Exception e: print(e)
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
    data_store.create_file(b"", cwd + filename)


def delete(filename):
    data_store.delete_file(cwd + filename)


def mkdir(dirname):
    # TODO: Validate directory name
    data_store.create_filder(cwd + dirname)


def chdir(dirname):
    # Check if directory exists
    cwd += "dirname/"


def move(source_filename, target_filename):
    print("move")


def open_file(filename):
    print("open_file")


def close_file():
    print("close_file")


def write(text, at=0):
    print("write")


def read():
    print("read")


def move_within_file(start, size, target):
    print("move_within_file")


def truncate_file(max_size):
    print("truncate_file")


def show_mem_map():
    print("show_mem_map")


def exit():
    os.system("clear")
    quit()


if __name__ == "__main__": main()