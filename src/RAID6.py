from RAID_MATH import GaloisField
import numpy as np

class RAID6(object):
    def __init__(self, num_check_disk, num_data_disk):
        self.num_check_disk = num_check_disk
        self.num_data_disk = num_data_disk
        self.block_size = 4
        self.chunk_size = 32
        self.stripe_size = self.num_data_disk * self.chunk_size

        assert self.chunk_size % self.block_size == 0

        self.GF = GaloisField(self.num_check_disk, self.num_data_disk)
        self.data_disk_list=list(range(self.num_data_disk))
        self.check_disk_list = list(range(self.num_check_disk))
        self.file_map = {}


    def write_data(self, filename):
        with open(filename, "rb") as f:
            content = f.read()
            content = list(content)
            file_real_length = len(content)
            stripe = file_real_length // self.stripe_size + 1
            file_padding_length = stripe * self.stripe_size

            for i in range(file_padding_length - file_real_length):
                content.append(0)

            for i in range(self.num_data_disk):
                with open("data_disk_{}".format(int(i)), 'wb') as f:
                    for j in range(stripe):
                        start_index = j * self.stripe_size + i * self.chunk_size
                        end_index = start_index + self.chunk_size
                        to_write = content[start_index : end_index]
                        f.write(bytes(to_write))

        self.file_map[filename] = {
            "filename" : filename,
            "file_real_length" : file_real_length,
            "file_padding_length" : file_padding_length
        }

        self.update_check_disk(self.chunk_size * stripe)

    def read_data(self, filename):
        try:
            file_real_length = self.file_map[filename]["file_real_length"]
            file_padding_length = self.file_map[filename]["file_padding_length"]
        except KeyError:
            return False

        file_content = [0 for i in range(file_padding_length)]
        stripe = file_real_length // self.stripe_size + 1
        for i in range(self.num_data_disk):
            with open("data_disk_{}".format(int(i)), 'rb') as f:
                disk_content = list(f.read())
                for j in range(stripe):
                    start_index = j * self.stripe_size + i * self.chunk_size
                    end_index = start_index + self.chunk_size
                    to_read = disk_content[j * self.stripe_size : (j + 1) * self.stripe_size]
                    file_content[start_index : end_index] = to_read

        print(filename, ":", bytes(file_content[:file_real_length]))

    def update_check_disk(self, data_disk_length):
        F = self.GF.F # data_disk by check_disk
        F = np.transpose(F) # check_disk by data_disk
        D = np.zeros([self.num_data_disk, data_disk_length], dtype=int)

        # D
        for i in range(self.num_data_disk):
            with open("data_disk_{}".format(int(i)), 'rb') as f:
                disk_content = list(f.read())
                D[i,:] = disk_content

        # C
        C = self.GF.matmul(F, D)

        for i in range(self.num_check_disk):
            with open("check_disk_{}".format(int(i)), "wb") as f:
                to_write = bytes(C[i,:])
                f.write(to_write)

    def int_to_byte(self):
        pass