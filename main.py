import os 
import numpy as np
import string
from data import DATA_PATH
from src.config import Config
from src.RAID6 import RAID6

def main(test_obj):
    # initialize configuration
    init = Config()
    dir = init.mkdisk()

    # setup RAID6 controller
    controller = RAID6(init)
    original_data = open(os.path.join(DATA_PATH, test_obj), 'r').read()
    print("original data: "+str(original_data))

    # write data objects across storage nodes
    controller.write_to_disk(os.path.join(DATA_PATH, test_obj), dir)

    # rebuild lost redundancy
    controller.rebuild_data(dir, corrupted_disk_list=[2,3])
    controller.read_from_disk(dir)

if __name__ == "__main__":
    test_obj = 'test.txt'
    main(test_obj)