from RAID6 import RAID6
import time
import matplotlib.pyplot as plt
#
# write_time = []
# recover_time = []
# read_time = []
# chunk_sizes = []
#
# for i in range(4,9):
#     chunk_size = 2 ** i
#     chunk_sizes.append(chunk_size)
#     R = RAID6(
#         num_check_disk=2,
#         num_data_disk=6,
#         chunk_size=chunk_size
#     )
#     start_time = time.time()
#     R.write_data("test.jpg")
#     end_time = time.time()-start_time
#     write_time.append(end_time)
#
#     R.lost_disk([1,2])
#     start_time = time.time()
#     R.recover("test.jpg", [1,2])
#     end_time = time.time()-start_time
#     recover_time.append(end_time)
#
#     start_time = time.time()
#     content = R.read_data("test.jpg")
#     end_time = time.time()-start_time
#     read_time.append(end_time)
#
# plt.figure(dpi=200)
# plt.plot(chunk_sizes, write_time,color='blue', label="Write Time")
# plt.plot(chunk_sizes, read_time,color='red', label="Read Time")
# plt.plot(chunk_sizes, recover_time,color='green', label="Recover Time")
# plt.title("Time on different chunk size")
# plt.xlabel("Chunk size (Bytes)")
# plt.ylabel("Time (Seconds)")
# plt.legend()
# plt.savefig("result.png")
#
# # with open("out.jpg",'wb') as f:
# #     f.write(bytes(content))


# write_time = []
# recover_time = []
# read_time = []
# num_check_disks = list(range(2,9))
#
# for i in num_check_disks:
#
#     R = RAID6(
#         num_check_disk=i,
#         num_data_disk=10-i,
#         chunk_size=256
#     )
#     start_time = time.time()
#     R.write_data("test.jpg")
#     end_time = time.time()-start_time
#     write_time.append(end_time)
#
#     R.lost_disk([1,2])
#     start_time = time.time()
#     R.recover("test.jpg", [1,2])
#     end_time = time.time()-start_time
#     recover_time.append(end_time)
#
#     start_time = time.time()
#     content = R.read_data("test.jpg")
#     end_time = time.time()-start_time
#     read_time.append(end_time)
#
# plt.figure(dpi=200)
# plt.plot(num_check_disks, write_time,color='blue', label="Write Time")
# plt.plot(num_check_disks, read_time,color='red', label="Read Time")
# plt.plot(num_check_disks, recover_time,color='green', label="Recover Time")
# plt.title("Time on different number of parity disks")
# plt.xlabel("Number of parity disks")
# plt.ylabel("Time (Seconds)")
# plt.legend()
# plt.savefig("result-parity-disks.png")




R = RAID6(
    num_check_disk=3,
    num_data_disk=6,
    chunk_size=16
)

R.write_data("test.txt")
R.lost_disk([1,2])
R.recover("test.txt", [1,2])
content = R.read_data("test.txt")
with open("out.txt", 'wb') as f:
    f.write(bytes(content))
print(str(bytes(content)))
