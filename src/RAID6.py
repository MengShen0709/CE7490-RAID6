import os
import numpy as np
from src.ffield import GaloisField

class RAID6(object):
    '''
    A class for RAID6 controller
    '''
    def __init__(self, config):
        self.config = config
        self.gf = GaloisField(num_data_disk = self.config.num_data_disk,
                              num_check_disk= self.config.num_check_disk)

        self.data_disk_list  = list(range(self.config.num_data_disk))
        self.check_disk_list = list(range(self.config.num_data_disk, \
                                          self.config.num_data_disk+self.config.num_check_disk))

        print("controller activated, ready to store data\n")
        input("Press Enter to continue ...\n")
    
    def read_data(self, filename, mode = 'rb'):
        with open(filename, mode) as f:
            return list(f.read())
    
    def distribute_data(self, filename):
        '''split data to different disk
        :param filename:
        :return: data array
        '''
        content = self.read_data(filename)
        self.content_length = len(content)
        file_size = len(content)
        total_stripe = file_size // self.config.stripe_size + 1
        total_stripe_size = total_stripe * self.config.stripe_size
        # zero-padding
        content = content + [0] * (total_stripe_size - file_size)
        content = np.asarray(content, dtype=int)
        content = content.reshape(self.config.num_data_disk, \
                                  self.config.chunk_size * total_stripe)

        return content
    
    def compute_parity(self, content):
        '''compute parity based on current data words
        :param content: data words
        :return: checksum words
        '''
        return self.gf.matmul(self.gf.vander, content)
    
    def write_to_disk(self, filename, dir):
        '''concurrently write data and checksum words to each disk
        :param filename:
        :param dir:
        :return:
        '''
        data = self.distribute_data(filename)
        parity = self.compute_parity(data)
        data_with_parity = np.concatenate([data, parity], axis=0)
        for i in range(self.config.num_disk):
            with open(os.path.join(dir, 'disk_{}'.format(i)), 'wb') as f:
                to_write = bytes(data_with_parity[i,:].tolist())
                f.write(to_write)
        print("write data and parity to disk successfully\n")
    
    def read_from_disk(self, dir):
        '''read data from each disk
        :param dir:
        :return: recovered content
        '''
        content = []
        for i in range(self.config.num_data_disk):
            with open(os.path.join(dir, "disk_{}".format(i)), 'rb') as f:
                content += list(f.read())
        # cut empty content          
        content = content[:self.content_length]
        
        return content
       
    def erase_disk(self, dir, erase_list):
        """
        erase the disks
        :param corrupted_disk_list: disks to be erased
        :return: None
        """
        for i in erase_list:
            os.remove(os.path.join(dir,"disk_{}".format(i)))
            print("\ndisk_{} is erased".format(i))

    def rebuild_data(self, dir, corrupted_disk_list):
        '''rebuild data from corrupted disk
        :param dir: disk directory
        :param corrupted_disk_list: corrupted disk
        :return: None
        '''
        
        input("\nPress Enter to rebuild lost data ...\n")

        if len(corrupted_disk_list) > self.config.num_check_disk:
            print("failed to rebuild data")
            return -1

        left_data = []
        left_parity = []
        left_data_disk = list(set(self.data_disk_list).difference(set(corrupted_disk_list)))
        left_check_disk= list(set(self.check_disk_list).difference(set(corrupted_disk_list)))

        for i in left_data_disk:
            left_data.append(self.read_data(os.path.join(dir,'disk_{}'.format(i))))
        for j in left_check_disk:
            left_parity.append(self.read_data(os.path.join(dir,'disk_{}'.format(j))))

        A = np.concatenate([np.eye(self.config.num_data_disk, dtype=int), self.gf.vander], axis=0)
        A_= np.delete(A, obj=corrupted_disk_list, axis=0)

        E_= np.concatenate([np.asarray(left_data), np.asarray(left_parity)], axis=0)

        D = self.gf.matmul(self.gf.inverse(A_), E_)
        C = self.gf.matmul(self.gf.vander, D)

        E = np.concatenate([D, C], axis=0)

        for i in corrupted_disk_list:
            with open(os.path.join(dir,'disk_{}'.format(i)), 'wb') as f:
                to_write = bytes(E[i,:].tolist())
                f.write(to_write)
        
        print("rebuild data successfully\n")