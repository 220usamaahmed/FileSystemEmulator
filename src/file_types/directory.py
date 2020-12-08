import pickle


class Directory():

    def __init__(self, name=None, address=None, parent_address=None,
        files=None, sub_directories=None):
        if files == None: files = {}
        if sub_directories == None: sub_directories = {}
        self.name = name
        self.address = address
        self.parent_address = parent_address
        self.files = files
        self.sub_directories = sub_directories


    def __repr__(self):
        return \
        "------ Directory -------\n" \
        f"Name:\n{self.name}\n\n" \
        f"Address:\n{self.address}\n\n" \
        f"Parent Address:\n{self.parent_address}\n\n" \
        f"Files:\n{self.files}\n\n" \
        f"Sub Directories:\n{self.sub_directories}\n\n"


    def dump(self):
        return pickle.dumps({
            "files": self.files,
            "sub_directories": self.sub_directories,
        })

    
    def load(dumped_bytes, name, address, parent_address):
        data = pickle.loads(dumped_bytes)
        return Directory(name, address, parent_address, data["files"],
            data["sub_directories"])


    def add_sub_directory_record(self, sub_directory_name, address):
        if sub_directory_name.isalnum():
            if not self.sub_directory_exists(sub_directory_name):
                self.sub_directories[sub_directory_name] = address
            else:
                raise Exception("This directory already exists.")
        else:
            raise Exception("Directory's name should be alpha numeric.")

    
    def add_file_record(self, file_name, address):
        if file_name.isalnum():
            if not self.file_exists(file_name):
                self.files[file_name] = address
            else:
                raise Exception("This file already exists.")
        else:
            raise Exception("File's name should be alpha numeric.")


    def remove_file_record(self, file_name):
        if file_name in self.files:
            del self.files[file_name]
        else:
            raise Exception("This file does not exist.")


    def file_exists(self, file_name):
        return file_name in self.files


    def sub_directory_exists(self, sub_directory_name):
        return sub_directory_name in self.sub_directories


    def get_file_address(self, file_name):
        if self.file_exists(file_name):
            return self.files[file_name]
        else:
            raise Exception("This file does not exist")


    def get_sub_directory_address(self, sub_directory_name):
        if self.sub_directory_exists(sub_directory_name):
            return self.sub_directories[sub_directory_name]
        else:
            raise Exception("This sub-directory does not exist")

    
    def list_files(self):
        return self.files.keys()


    def list_sub_directories(self):
        return self.sub_directories.keys()