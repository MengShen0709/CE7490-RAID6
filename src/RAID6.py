import os
import numpy as np
from src.ffield import GaloisField

class RAID6(object):
    def __init__(self, config):
        self.config = config
        self.gf = GaloisField(num_data_disk=self.config.num_data_disk,
                              num_check_disk=self.config.num_check_disk)

        self.data_disk_list=list(range(self.config.num_data_disk))
        self.check_disk_list = list(range(self.config.num_check_disk))
    
    def read_data(self, filename, mode = 'rb'):
        with open(filename, mode) as f:
            return list(f.read())
    
    def distribute_data(self, filename):
        content = self.read_data(filename)
        file_size = len(content)
        total_stripe = file_size // self.config.stripe_size + 1
        total_stripe_size = total_stripe * self.config.stripe_size
        # zero-padding  
        for i in range(total_stripe_size - file_size):
            content.append(0)
        content = np.asarray(content)
        content = content.reshape(self.config.num_data_disk, \
                                  self.config.chunk_size * total_stripe)

        return content
    
    def compute_parity(self, content):
        data = content
        vander = self.gf.vander
        parity = self.gf.matmul(vander, data)

        return parity
    
    def write_to_disk(self, filename, dir):
        data = self.distribute_data(filename)
        parity = self.compute_parity(data)
        data_with_parity = np.concatenate([data, parity], axis=0)
        for i in range(self.config.num_disk):
            with open(os.path.join(dir, 'disk_{}'.format(i)), 'wb') as f:
                f.write(bytes(data_with_parity[i,:]))
       
    def check_failure(self):
        
        pass

    def rebuild_data(self):
        pass


    # def write_data(self, filename, data):
    #     with open(filename, "wb") as w:
    #         w.write(data)
    #     with open(filename, "rb") as f:    
    #         content = f.read()
    #         content = list(content)
    #         file_real_length = len(content)
    #         stripe = file_real_length // self.config.stripe_size + 1
    #         file_padding_length = stripe * self.config.stripe_size

    #         for i in range(file_padding_length - file_real_length):
    #             content.append(0)

    #         for i in self.data_disk_list:
    #             with open(os.path.join(filename,"data_disk_{}".format(int(i))), 'wb') as f:
    #                 for j in range(stripe):
    #                     start_index = j * self.config.stripe_size + i * self.config.chunk_size
    #                     end_index = start_index + self.config.chunk_size
    #                     to_write = content[start_index : end_index]
    #                     f.write(bytes(to_write))

    #     self.file_map[filename] = {
    #         "filename" : filename,
    #         "file_real_length" : file_real_length,
    #         "file_padding_length" : file_padding_length
    #     }

    #     self.update_check_disk(self.config.chunk_size * stripe)

    # def read_data(self, filename):
    #     try:
    #         file_real_length = self.file_map[filename]["file_real_length"]
    #         file_padding_length = self.file_map[filename]["file_padding_length"]
    #     except KeyError:
    #         return False

    #     file_content = [0 for i in range(file_padding_length)]
    #     stripe = file_real_length // self.config.stripe_size + 1
    #     for i in self.data_disk_list:
    #         with open(os.path.join(filename,"data_disk_{}".format(int(i))), 'rb') as f:
    #             disk_content = list(f.read())
    #             for j in range(stripe):
    #                 start_index = j * self.config.stripe_size + i * self.config.chunk_size
    #                 end_index = start_index + self.config.chunk_size
    #                 to_read = disk_content[j * self.config.chunk_size : (j + 1) * self.config.chunk_size]
    #                 file_content[start_index : end_index] = to_read

    #     print(filename, ":", bytes(file_content[:file_real_length]))

    # def update_check_disk(self, data_disk_length):
    #     F = self.gf.vander # data_disk by check_disk
    #     D = np.zeros([self.config.num_data_disk, data_disk_length], dtype=int)

    #     # D
    #     for i in self.data_disk_list:
    #         with open("data_disk_{}".format(int(i)), 'rb') as f:
    #             disk_content = list(f.read())
    #             D[i,:] = disk_content

    #     # C
    #     C = self.gf.matmul(F, D)

    #     for i in self.check_disk_list:
    #         with open("check_disk_{}".format(int(i)), "wb") as f:
    #             to_write = bytes(C[i,:].tolist())
    #             f.write(to_write)

    #     self.data_disk_length = data_disk_length

    # def recover(self, data_disk_lost_list=None, check_disk_lost_list=None):

    #     lost_data_disk_list = [1]
    #     lost_check_disk_list = [1]
    #     print("removed data disks:", lost_data_disk_list)
    #     print("removed check disks:", lost_check_disk_list)
    #     recover_data_disk_list = [i for i in self.data_disk_list if i not in lost_data_disk_list]
    #     recover_check_disk_list = [i for i in self.check_disk_list if i not in lost_check_disk_list]

    #     D = np.zeros([len(recover_data_disk_list), self.data_disk_length], dtype=int)
    #     index = 0
    #     for i in recover_data_disk_list:
    #         with open("data_disk_{}".format(int(i)), 'rb') as f:
    #             disk_content = list(f.read())
    #             D[index,:] = disk_content
    #         index += 1

    #     C = np.zeros([len(recover_check_disk_list), self.data_disk_length], dtype=int)
    #     index = 0
    #     for i in recover_check_disk_list:
    #         with open("check_disk_{}".format(int(i)), 'rb') as f:
    #             disk_content = list(f.read())
    #             C[index,:] = disk_content
    #         index += 1

    #     E = np.concatenate((D, C), axis=0)
        
    #     A = np.concatenate(np.eye(self.config.num_data_disk, dtype=int), self.gf.vander, axis=0)
    #     to_remove = lost_data_disk_list + [i + self.config.num_data_disk for i in lost_check_disk_list]
    #     A_ = np.delete(A,obj=to_remove, axis=0)
    #     A_inverse = self.gf.inverse(A_)
    #     D_ = self.gf.matmul(A_inverse, E)
    #     C_ = self.gf.matmul(self.gf.vander, D_)

    #     for i in lost_data_disk_list:
    #         with open("data_disk_{}".format(int(i)), 'wb') as f:
    #             to_write = bytes(D_[i,:].tolist())
    #             f.write(to_write)

    #     for i in lost_check_disk_list:
    #         with open("check_disk_{}".format(int(i)), 'wb') as f:
    #             to_write = bytes(C_[i,:].tolist())
    #             f.write(to_write)

    #     print("recovered")


    # def int_to_byte(self):
    #     pass