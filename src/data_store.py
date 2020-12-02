from os import path

import config
from src.block import Block
from src.descriptor import Descriptor

import pickle


class DataStore:

    def __init__(self, filepath):
        self.filepath = filepath
        self.descriptor = None

        if path.exists(filepath):
            print(f"Loading existing data store at {filepath}")
            self.load_descriptor()
        else:
            print(f"Creating new data store at {filepath}")
            self.create_new()


    def create_new(self):
        with open(self.filepath, 'w'): pass
        
        self.descriptor = Descriptor()
        block_sequnce = self.generate_block_sequnce(self.descriptor.dump())
        self.save_block_sequence(block_sequnce, 0)


    def generate_block_sequnce(self, data):
        block_sequnce = []
        if len(data):
            for i in range(0, len(data), config.USABLE_BLOCK_SIZE):
                block = Block.new(data[i:i+config.USABLE_BLOCK_SIZE])
                if i < len(data) - config.USABLE_BLOCK_SIZE:
                    block.set_next_block(self.descriptor.get_empty_block())
                block_sequnce.append(block)
        else:
            block_sequnce.append(Block.new(b""))

        return block_sequnce


    def save_block_sequence(self, block_sequnce, starting_addr):
        with open(self.filepath, 'r+b') as f:
            f.seek(starting_addr)
            for block in block_sequnce:
                f.write(block.get_bytes())
                if not block.is_last:
                    f.seek(Descriptor.address_from_id(block.next_block_id))


    def load_block_sequnce(self, starting_addr):
        block_sequnce = []

        with open(self.filepath, 'rb') as f:
            f.seek(starting_addr)

            while True:
                block_bytes = f.read(config.BLOCK_SIZE)
                block = Block.load(block_bytes)
                block_sequnce.append(block)

                if not block.is_last:
                    f.seek(Descriptor.address_from_id(block.next_block_id))
                else: break

        return block_sequnce

    
    def replace_block_sequnce(self, data, starting_addr):
        # Clear old block sequence except for first block
        block_sequnce = self.load_block_sequnce(starting_addr)
        for block in block_sequnce:
            if not block.is_last:
                self.descriptor.add_dead_block(block.next_block_id)
        
        # Save new block sequnce starting by overwriting that old starting block
        block_sequnce = self.generate_block_sequnce(data)
        self.save_block_sequence(block_sequnce, starting_addr)


    def load_descriptor(self):
        descriptor_block_sequnce = self.load_block_sequnce(0)
        self.descriptor = Descriptor.load(
            b"".join([block.get_data() for block in descriptor_block_sequnce])
        )


    def create_file(self, data, path):
        if path in self.descriptor.index:
            raise Exception("This file already exists.")

        # Add new file to descriptor
        starting_addr = Descriptor.address_from_id(self.descriptor.get_empty_block())
        block_sequnce = self.generate_block_sequnce(data)
        self.descriptor.add_file(path, starting_addr)

        # Update descriptor blocks
        self.replace_block_sequnce(self.descriptor.dump(), 0)

        # Save new file descriptor blocks
        self.save_block_sequence(block_sequnce, starting_addr)


    def read_file(self, path):
        block_sequnce = self.load_block_sequnce(self.descriptor.get_address(path))
        return b"".join([block.get_data() for block in block_sequnce])


    def update_file(self, data, path):
        self.replace_block_sequnce(data, self.descriptor.get_address(path))


    def delete_file(self, path):
        starting_addr = self.descriptor.get_address(path)
        block_sequnce = self.load_block_sequnce(starting_addr)
        self.descriptor.add_dead_block(Descriptor.id_from_address(starting_addr))
        for block in block_sequnce:
            if not block.is_last:
                self.descriptor.add_dead_block(block.next_block_id)
        self.descriptor.remove_file(path)
        self.replace_block_sequnce(self.descriptor.dump(), 0)


    def move_file(self, source_filepath, target_filepath):
        self.descriptor.move_file(source_filepath, target_filepath)


    def create_directory(self, path):
        self.descriptor.add_directory(path)
        self.replace_block_sequnce(self.descriptor.dump(), 0)