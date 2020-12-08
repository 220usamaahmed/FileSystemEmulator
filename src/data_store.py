from os import path

import config
from src.block import Block
from src.file_types.block_manager import BlockManager
from src.file_types.directory import Directory
from src.file_types.generic import Generic

import pickle


class DataStore:

    #########################
    ## Initialization Code ##
    #########################

    def __init__(self, filepath):
        self.filepath = filepath
        self.block_manager = None
        self.root_directory = None

        if path.exists(filepath):
            # print(f"Loading existing data store at {filepath}\n")
            self.load_block_manager()
            self.load_root_directory()
        else:
            # print(f"Creating new data store at {filepath}\n")
            self.create_new()


    def create_new(self):
        with open(self.filepath, 'w'): pass
        
        # Creating a new block manager
        self.block_manager = BlockManager()
        block_sequnce = self.generate_block_sequnce(self.block_manager.dump())
        self.save_block_sequence(block_sequnce, BlockManager.address_from_id(
            config.BLOCK_MANAGER_RESERVED_BLOCK
        ))

        # Creating a new root directory
        root_directory_address = BlockManager.address_from_id(
            config.ROOT_DIRECTORY_RESERVED_BLOCK)
        self.root_directory = Directory(name="root", 
            address=root_directory_address)
        block_sequnce = self.generate_block_sequnce(self.root_directory.dump())
        self.save_block_sequence(block_sequnce, root_directory_address)

    
    def load_block_manager(self):
        self.block_manager = BlockManager.load(self.sequential_read(
            BlockManager.address_from_id(
                config.BLOCK_MANAGER_RESERVED_BLOCK
        )))


    def load_root_directory(self):
        address = BlockManager.address_from_id(
            config.ROOT_DIRECTORY_RESERVED_BLOCK)
        self.root_directory = Directory.load(self.sequential_read(address),
            "root", address, None)


    ####################################
    ## Block Sequence Management Code ##
    ####################################

    def generate_block_sequnce(self, data):
        block_sequnce = []
        if len(data):
            for i in range(0, len(data), config.USABLE_BLOCK_SIZE):
                block = Block.new(data[i:i+config.USABLE_BLOCK_SIZE])
                if i < len(data) - config.USABLE_BLOCK_SIZE:
                    block.set_next_block(self.block_manager.get_empty_block())
                block_sequnce.append(block)
        else:
            block_sequnce.append(Block.new(b""))

        return block_sequnce


    def save_block_sequence(self, block_sequnce, address):
        with open(self.filepath, 'r+b') as f:
            f.seek(address)
            for block in block_sequnce:
                f.write(block.get_bytes())
                if not block.is_last:
                    f.seek(
                        BlockManager.address_from_id(block.next_block_id))


    def load_block_sequnce(self, address):
        block_sequnce = []

        with open(self.filepath, 'rb') as f:
            f.seek(address)

            while True:
                block_bytes = f.read(config.BLOCK_SIZE)
                block = Block.load(block_bytes)
                block_sequnce.append(block)

                if not block.is_last:
                    f.seek(BlockManager.address_from_id(block.next_block_id))
                else: break

        return block_sequnce

    
    def replace_block_sequnce(self, data, address):
        # Clear old block sequence except for first block
        block_sequnce = self.load_block_sequnce(address)
        for block in block_sequnce:
            if not block.is_last:
                self.block_manager.add_dead_block(block.next_block_id)
        
        # Save new block sequnce starting by overwriting that old 
        # starting block
        block_sequnce = self.generate_block_sequnce(data)
        self.save_block_sequence(block_sequnce, address)


    def sequential_read(self, address):
        block_sequnce = self.load_block_sequnce(address)
        return b"".join([block.get_data() for block in block_sequnce])


    def update_block_manager(self):
        self.replace_block_sequnce(self.block_manager.dump(), 
            config.BLOCK_MANAGER_RESERVED_BLOCK)


    ##########################
    ## File Opeartions Code ##
    ##########################
    
    def create_directory(self, parent, directory_name):
        if parent.sub_directory_exists(directory_name):
            raise Exception("This directory already exists.")

        # Update and save block manager and parent
        address = BlockManager.address_from_id(
            self.block_manager.get_empty_block())
        parent.add_sub_directory_record(directory_name, address)
        self.replace_block_sequnce(parent.dump(), parent.address)
        self.update_block_manager()

        # Create new sub-directory and save it
        new_directory = Directory(name=directory_name, address=address,
            parent_address=parent.address)
        block_sequnce = self.generate_block_sequnce(new_directory.dump())
        self.save_block_sequence(block_sequnce, address)

        return new_directory

    
    def load_directory(self, parent, sub_directory_name):
        address = parent.get_sub_directory_address(sub_directory_name)
        return Directory.load(self.sequential_read(address),
            sub_directory_name, address, parent.address)


    def create_file(self, parent, file_name, data):
        if parent.file_exists(file_name):
            raise Exception("This file already exists.")

        # Update and save block manager and parent
        address = BlockManager.address_from_id(
            self.block_manager.get_empty_block())
        parent.add_file_record(file_name, address)
        self.replace_block_sequnce(parent.dump(), parent.address)
        self.update_block_manager()

        # Create new file and save it
        new_file = Generic(data, file_name, address, parent.address)
        block_sequnce = self.generate_block_sequnce(new_file.dump())
        self.save_block_sequence(block_sequnce, address)

        return new_file


    def load_file(self, directory, file_name):
        address = directory.get_file_address(file_name)
        return Generic(self.sequential_read(address), file_name, address,
            directory.address)


    def save_updated_file(self, file):
        self.replace_block_sequnce(file.dump(), file.address)


    def delete_file(self, directory, file_name):
        address = directory.get_file_address(file_name)
        
        block_sequnce = self.load_block_sequnce(address)
        self.block_manager.add_dead_block(
            BlockManager.id_from_address(address))
        for block in block_sequnce:
            if not block.is_last:
                self.block_manager.add_dead_block(block.next_block_id)
        self.update_block_manager()

        directory.remove_file_record(file_name)
        self.replace_block_sequnce(directory.dump(), directory.address)


    def move_file(self, source_directory, destination_directory, file_name):
        if destination_directory.file_exists(file_name):
            raise Exception("A file with this name already exists in" \
                f"{destination_directory.name}")
        else:
            address = source_directory.get_file_address(file_name)
            source_directory.remove_file_record(file_name)
            destination_directory.add_file_record(file_name, address)
            self.replace_block_sequnce(source_directory.dump(),
                source_directory.address)
            self.replace_block_sequnce(destination_directory.dump(),
                destination_directory.address)