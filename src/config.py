import time
import os
from data import DATA_PATH

class Config(object):

    def __init__(self):
        self.num_disk = 8
        self.num_data_disk = 6
        self.num_check_disk = 2

        assert self.num_disk == self.num_data_disk + self.num_check_disk

        self.block_size = 4
        self.chunk_size = 16
        self.stripe_size = self.num_data_disk * self.chunk_size
        
        assert self.chunk_size % self.block_size == 0

        print("Num of Disk: %d" % self.num_disk)
        print("Num of Data Disk: %d" % self.num_data_disk)
        print("Num of Checksum: %d" % self.num_check_disk)
        
    
    def mkdisk(self):
        test_dir = os.path.join(DATA_PATH, time.strftime('%Y-%m-%d %H-%M-%S'))
        os.mkdir(test_dir)
        return test_dir
        

