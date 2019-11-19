from RAID6 import RAID6

R = RAID6(
    num_check_disk=2,
    num_data_disk=6
)
R.write_data("src/test.txt")
R.read_data("src/test.txt")
