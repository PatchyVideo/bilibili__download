from config import Config
import psycopg2

class Bv2av(object):

    table = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
    tr = {}
    s = [11, 10, 3, 8, 4, 6]
    xor = 177451812
    add = 8728348608

    def __init__(self):
        for i in range(58):
            self.tr[self.table[i]] = i


    def dec(self, x):
        """bv2av"""
        r = 0
        for i in range(6):
            r += self.tr[x[self.s[i]]] * 58 ** i
        return (r - self.add) ^ self.xor


    def enc(self, x):
        """av2bv"""
        x = (x ^ self.xor) + self.add
        r = list('BV1  4 1 7  ')
        for i in range(6):
            r[self.s[i]] = self.table[x // 58 ** i % 58]
        return ''.join(r)


class DbBase():

    def __init__(self):
        self.connection = psycopg2.connect(database=Config.database, user=Config.user, password=Config.password, host=Config.host, port=Config.port)
        self.cursor = self.connection.cursor()


    def close(self):
        self.connection.close()


