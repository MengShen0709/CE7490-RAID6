from src.RAID6 import RAID6

num_parity_disk = 2
num_data_disk = 10
chunk_size = 1024 # in Bytes

R = RAID6(
    num_check_disk=num_parity_disk,
    num_data_disk=num_data_disk,
    chunk_size=chunk_size
)

lost_list = list(range(num_parity_disk))
R.write_data("test.jpg")
R.erase_disk(lost_list)
R.recover("test.jpg", lost_list)
content = R.read_data("test.jpg")
with open("out.jpg", 'wb') as f:
    f.write(bytes(content))

