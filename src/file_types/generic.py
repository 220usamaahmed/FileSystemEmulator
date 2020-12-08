class Generic():

    def __init__(self, data=b"", name=None, address=None, parent_address=None):
        self.data = data
        self.name = name
        self.address = address
        self.parent_address = parent_address


    def __repr__(self):
        return self.name


    def get_data(self):
        return self.data


    def dump(self):
        return self.data


    def write_at(self, data_to_write, at):
        self.data = self.data[:at] \
            + data_to_write \
            + self.data[len(data_to_write) + at:]


    def append(self, data_to_write):
        self.data += data_to_write


    def move_within(self, start, size, target):
        self.write_at(self.data[start:start + size], target)

    
    def truncate(self, at):
        self.data = self.data[:at]
