import numpy as np

PRIM_POLY = 285  # 0x11D  x^8+x^4+x^3+x^2+1
G_F = 8


class GaloisField(object):
    def __init__(self, num_data_disk, num_check_disk):
        self.num_check_disk = num_check_disk
        self.num_data_disk = num_data_disk
        self.G_Range = 2 ** G_F
        self.j_to_xj = list(range(self.G_Range))
        self.xj_to_j = list(range(self.G_Range))
        self.F = np.zeros([self.num_check_disk, self.num_data_disk], dtype=int)
        self.init_log_table()
        self.init_F()

    def multiply(self, a, b):
        """
        c = a * b
          = x^aj * x^bj
          = x^((aj + bj) mod 255)
          = x^cj
        :return: c
        """
        if a == 0 or b == 0:
            return 0
        aj = self.xj_to_j[a]
        bj = self.xj_to_j[b]
        cj = (aj + bj) % (self.G_Range - 1)
        c = self.j_to_xj[cj]
        return c

    def devide(self, a, b):
        """
        c = a / b
          = x^aj / x^bj
          = x^((aj - bj) mod 255)
          = x^cj
        :return: c
        """
        if a == 0:
            return 0
        if b == 0:
            return None
        aj = self.xj_to_j[a]
        bj = self.xj_to_j[b]
        cj = (aj - bj) % (self.G_Range - 1)
        c = self.j_to_xj[cj]
        return c

    def power(self, a, n):
        """
        an = a^n
        :return: an
        """
        n = n % (self.G_Range - 1)  # if n == 0 return 1
        an = 1
        for i in range(n):
            an = self.multiply(an, a)
        return an

    def init_log_table(self):
        """
        x = 2
        xj = x^j
        """
        xj = 1
        for j in range(self.G_Range - 1):
            self.j_to_xj[j] = xj
            self.xj_to_j[xj] = j
            xj = xj << 1
            if xj & self.G_Range:
                xj = xj ^ PRIM_POLY
        self.j_to_xj[self.G_Range - 1] = None
        self.xj_to_j[0] = None


    def init_F(self):
        """
        generate the F vandermonde matrix (m by n)
        :return:
        """
        for m in range(self.num_check_disk):
            for n in range(self.num_data_disk):
                self.F[m][n] = self.power(n + 1, m)

    def add(self, a, b):
        c = a ^ b
        return c

    def dot(self, a, b):
        """
        c = dot(a,b)
        :return: c
        """
        c = 0
        for i in range(len(a)):
            c = self.add(c, self.multiply(a[i], b[i]))
        return c

    def matmul(self, a, b):
        """
        mat c = mat a * mat b
        :return: mat c
        """
        c = np.zeros([a.shape[0], b.shape[1]], dtype=int)
        for i in range(c.shape[0]):
            for j in range(c.shape[1]):
                c[i][j] = self.dot(a[i,:], b[:,j])
        return c







