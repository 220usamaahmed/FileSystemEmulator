import config
import pickle

class Descriptor():

    def __init__(self, index={}, dead_block_ids=[], largest_used_id=0):
        self.index = index
        self.dead_block_ids = dead_block_ids
        self.largest_used_id = largest_used_id


    def __repr__(self):
        return "------ Descriptor Block -------\n" \
        f"Index:\n{self.index}\n\n" \
        f"Dead Block IDs:\n{self.dead_block_ids}\n\n" \
        f"Largest Used Block ID:\n{self.largest_used_id}\n" \
        "--- End of Descriptor Block ---"


    def dump(self):
        return pickle.dumps({
            "index": self.index,
            "dead_block_ids": self.dead_block_ids,
            "largest_used_id": self.largest_used_id
        })


    def load(dumped_bytes):
        data = pickle.loads(dumped_bytes)
        return Descriptor(
            data["index"], data["dead_block_ids"], data["largest_used_id"]
        )
    

    def get_empty_block(self):
        if self.dead_block_ids:
            return self.dead_block_ids.pop() 
        else:
            self.largest_used_id += 1
            return self.largest_used_id


    def add_dead_block(self, dead_block_id):
        self.dead_block_ids.append(dead_block_id)


    def add_file(self, path, starting_addr):
        # TODO: Check if filename and path are valid
        self.index[path] = starting_addr


    def add_directory(self, path):
        # TODO: Check if dirname and path are valid
        self.index[path] = None


    def remove_file(self, path):
        if not path in self.index:
            raise Exception("This file does not exist.")
        
        del self.index[path]


    def get_address(self, path):
        if not path in self.index:
            raise Exception("This file does not exist.")

        return self.index[path]


    def address_from_id(id):
        return id * config.BLOCK_SIZE


    def id_from_address(addr):
        return addr // config.BLOCK_SIZE