from RAID_MATH import GaloisField
import numpy as np
import os

class RAID6(object):
    def __init__(self, num_check_disk, num_data_disk, chunk_size):
        self.num_check_disk = num_check_disk
        self.num_data_disk = num_data_disk
        self.num_disk = self.num_check_disk + self.num_data_disk
        self.block_size = 4
        self.chunk_size = chunk_size
        self.stripe_size = self.num_data_disk * self.chunk_size
        assert self.chunk_size % self.block_size == 0
        self.GF = GaloisField(num_data_disk=self.num_data_disk, num_check_disk=self.num_check_disk)
        self.file_map = {}
        for i in range(self.num_disk):
            if os.path.isfile("disk_{}".format(i)):
                os.remove("disk_{}".format(i))

    def write_data(self, filename):
        f = open(filename, 'rb')
        file_real_length = 0
        file_padding_length = 0
        stripe_num = 0
        while True:
            content = list(f.read(self.stripe_size))
            content_length = len(content)
            if content_length == 0:
                break
            file_real_length += content_length
            # padding
            if content_length < self.stripe_size:
                content += [0] * (self.stripe_size - content_length)

            file_padding_length += self.stripe_size
            self.write_to_disk(content, stripe_num)
            stripe_num += 1

        f.close()
        self.file_map[filename] = {
            "filename" : filename,
            "file_real_length" : file_real_length,
            "file_padding_length" : file_padding_length,
            "stripe_num" : stripe_num
        }

    def write_to_disk(self, content, stripe_num):
        content = np.asarray(content)
        content = np.reshape(content, (self.num_data_disk, self.chunk_size))
        parity = self.GF.matmul(self.GF.F, content)
        data_with_parity = np.concatenate([content, parity], axis=0)
        for i in range(self.num_disk):
            index = (i + stripe_num) % self.num_disk
            with open('disk_{}'.format(index), 'ab') as f:
                to_write = bytes(data_with_parity[i, :].tolist())
                f.write(to_write)


    def read_data(self, filename):
        try:
            file_real_length = self.file_map[filename]["file_real_length"]
            stripe_num = self.file_map[filename]["stripe_num"]
        except KeyError:
            return False

        file_content = []
        for index in range(stripe_num):
            to_read_disk_index = [(i + index) % self.num_disk for i in range(self.num_data_disk)]
            seek_position = self.chunk_size * index
            for x in to_read_disk_index:
                with open("disk_{}".format(x), 'rb') as f:
                    f.seek(seek_position, 0)
                    content = f.read(self.chunk_size)
                    file_content += content

        return file_content[:file_real_length]


    def recover(self, filename, lost_list):

        try:
            stripe_num = self.file_map[filename]["stripe_num"]
        except KeyError:
            return False
        for index in range(stripe_num):
            seek_position = index * self.chunk_size
            data_disk_list, check_disk_list, disk_index \
                = self.get_disk_position(index, lost_list)
            D = self.read_data_from_disk(data_disk_list, seek_position)
            C = self.read_data_from_disk(check_disk_list, seek_position)
            if data_disk_list:
                E = np.concatenate((D, C), axis=0)
                A = np.concatenate((np.eye(self.num_data_disk, dtype=int), self.GF.F), axis=0)
                to_remove = [disk_index[i] for i in lost_list]
                A_ = np.delete(A, obj=to_remove, axis=0)
                A_inverse = self.GF.inverse(A_)
                D_ = np.zeros([self.num_data_disk, self.chunk_size], dtype=int)
                for iter, index in enumerate(data_disk_list):
                    row = disk_index[index]
                    D_[row, :] = D[iter, :]
                for index in lost_list:
                    row = disk_index[index]
                    if row < self.num_data_disk:
                        D_[row, :] = self.GF.matmul(A_inverse[row, :].reshape(
                            (1,self.num_disk - len(lost_list))), E)
            else:
                D_ = D

            C_ = self.GF.matmul(self.GF.F, D_)

            for i in lost_list:
                index = disk_index[i]
                with open("disk_{}".format(i), 'ab') as f:
                    if index < self.num_data_disk:
                        to_write = bytes(D_[index, :].tolist())
                    else:
                        to_write = bytes(C_[index - self.num_data_disk, :].tolist())
                    f.write(to_write)


    def lost_disk(self, lost_list):
        for i in lost_list:
            os.remove("disk_{}".format(i))

    def get_disk_position(self, stripe_num, lost_list=None):
        to_read_disk_index = [(i + stripe_num) % self.num_disk for i in range(self.num_disk)]
        data_disk_list = to_read_disk_index[:self.num_data_disk]
        check_disk_list = to_read_disk_index[self.num_data_disk:]
        if lost_list:
            disk_index = []
            for i in range(self.num_disk):
                disk_index.append(to_read_disk_index.index(i))
            data_disk_list = [i for i in data_disk_list if i not in lost_list]
            check_disk_list = [i for i in check_disk_list if i not in lost_list]
            return data_disk_list, check_disk_list, disk_index
        return data_disk_list, check_disk_list

    def read_data_from_disk(self, disk_list, seek_position):
        data = np.zeros([len(disk_list), self.chunk_size], dtype=int)
        index = 0
        for i in disk_list:
            with open("disk_{}".format(int(i)), 'rb') as f:
                f.seek(seek_position, 0)
                disk_content = list(f.read(self.chunk_size))
                data[index,:] = disk_content
            index += 1
        return data