from RAID6 import RAID6
import numpy as np

R = RAID6(
    num_check_disk=2,
    num_data_disk=6
)

R.write_data("src/test.txt")
R.read_data("src/test.txt")
R.recover()
R.read_data("src/test.txt")
