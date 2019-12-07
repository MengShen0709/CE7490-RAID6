import os 
import numpy as np
from data import DATA_PATH
from src.config import Config
from src.RAID6 import RAID6

def main(test_obj):
    # initialize configuration
    init = Config()
    dir = init.mkdisk()

    # setup RAID6 controller
    controller = RAID6(init)
    
    # write data objects across storage nodes
    original_data = open(os.path.join(DATA_PATH, test_obj), 'rb').read()
    #print("original data: "+str(original_data))

    controller.write_to_disk(os.path.join(DATA_PATH, test_obj), dir)

    # choose disk to erase arbitrarily
    corrupted_disk = [int(x) for x in input("choose disk to erase (split by space):").split()]
    controller.erase_disk(dir, corrupted_disk)

    # rebuild lost redundancy
    controller.rebuild_data(dir, corrupted_disk_list=corrupted_disk)
    content = controller.read_from_disk(dir)
    with open(os.path.join(DATA_PATH,'recovered.txt'), 'wb') as f:
        f.write(bytes(content))

if __name__ == "__main__":
    test_obj = 'test.txt'
    main(test_obj)