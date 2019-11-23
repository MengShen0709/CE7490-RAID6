from RAID6 import RAID6

num_check_disk = 2

R = RAID6(
    num_check_disk=num_check_disk,
    num_data_disk=10,
    chunk_size=256
)

lost_list = list(range(num_check_disk))
R.write_data("test.jpg")
R.lost_disk(lost_list)
R.recover("test.jpg", lost_list)
content = R.read_data("test.jpg")
with open("out.jpg", 'wb') as f:
    f.write(bytes(content))

