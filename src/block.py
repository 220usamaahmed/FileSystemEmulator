import config

IS_LAST_FLAG = 128
IS_NOT_LAST_FLAG = 0


class Block:

    def __init__(self, data=None, is_last=True):
        self.data_len = len(data)
        self.data = data.ljust(config.USABLE_BLOCK_SIZE)
        self.is_last = is_last
        self.next_block_id = None


    def set_next_block(self, next_block_id):
        if next_block_id > config.HEADER_BYTE_2 * 256 - 1:
            raise Exception("Next block ID has to be between 0 and 255")    
        self.is_last = False
        self.next_block_id = next_block_id


    def new(data):
        if len(data) > config.USABLE_BLOCK_SIZE:
            raise Exception(
                "Data passed greater than useable block size" \
                f"({config.USABLE_BLOCK_SIZE})"
            )
        else:
            return Block(data=data, is_last=True)


    def load(block_bytes):
        header_byte_1 = block_bytes[0]
        header_byte_2 = block_bytes[1]

        is_last = header_byte_1 & IS_LAST_FLAG == IS_LAST_FLAG
        data_len = header_byte_2 if is_last else config.USABLE_BLOCK_SIZE

        data = block_bytes[config.HEADER_SIZE:config.HEADER_SIZE + data_len]
        block = Block(data, is_last)
        if not is_last: block.set_next_block(header_byte_2)

        return block

        
    def get_data(self):
        return self.data[:self.data_len]


    def get_bytes(self):
        header_byte_1 = IS_LAST_FLAG.to_bytes(1, 'big') if self.is_last \
                        else IS_NOT_LAST_FLAG.to_bytes(1, 'big')
        header_byte_2 = self.data_len.to_bytes(1, 'big') if self.is_last \
                        else self.next_block_id.to_bytes(1, 'big')
                        
        return header_byte_1 + header_byte_2 + self.data