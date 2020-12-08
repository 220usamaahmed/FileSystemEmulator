import config
import pickle


class BlockManager():

    def __init__(self, dead_block_ids=None,
        largest_used_id=config.INITIAL_LARGEST_USED_ID):
        if dead_block_id == None: dead_block_id = []
        self.dead_block_ids = dead_block_ids
        self.largest_used_id = largest_used_id


    def __repr__(self):
        return \
        "------ Block Manager -------\n" \
        f"Dead Block IDs:\n{self.dead_block_ids}\n\n" \
        f"Largest Used Block ID:\n{self.largest_used_id}\n\n"


    def dump(self):
        return pickle.dumps({
            "dead_block_ids": self.dead_block_ids,
            "largest_used_id": self.largest_used_id
        })


    def load(dumped_bytes):
        data = pickle.loads(dumped_bytes)
        return BlockManager(
            data["dead_block_ids"],
            data["largest_used_id"]
        )
    

    def get_empty_block(self):
        if self.dead_block_ids:
            return self.dead_block_ids.pop() 
        else:
            self.largest_used_id += 1
            return self.largest_used_id


    def add_dead_block(self, dead_block_id):
        self.dead_block_ids.append(dead_block_id)


    def address_from_id(id):
        return id * config.BLOCK_SIZE


    def id_from_address(addr):
        return addr // config.BLOCK_SIZE