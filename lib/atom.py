import numpy as np
import copy


class Atom:

    # str and Atom are allowed as atom
    def __init__(self, atom=None, coodinate=None, TF=None, magmom=0, belong=None):
        self.name = None
        self.coodinate = np.array([0.0, 0.0, 0.0])
        self.TF = np.array([True, True, True])
        self.magmom = 0
        self.belong = None
        self.pdos = None
        if atom:
            if type(atom) is str:
                self.name = str(atom)
            elif type(atom) is Atom:
                self.__dict__ = copy.deepcopy(atom.__dict__)
            else:
                raise TypeError
        if coodinate:
            if type(coodinate) in (list, tuple, np.ndarray):
                self.coodinate = np.array(coodinate, float)
            else:
                raise TypeError
        if TF:
            if type(TF) in (list, tuple, np.ndarray):
                self.TF = np.array(TF, bool)
            else:
                raise TypeError
        if magmom:
            if type(magmom) in (int, float):
                self.magmom = magmom
            else:
                raise TypeError
        if belong:
            if type(belong) in (int, float, str):
                self.belong = str(belong)
            else:
                raise TypeError
        # return None

    def __setitem__(self, key, value):
        if key is 'coodinate':
            self.coodinate = np.array(value, dtype=float)
        elif key is 'TF':
            self.TF = np.array(value, dtype=bool)
            for i in range(3):
                if value[i] == 'F':
                    self.TF[i] = False
        elif key is 'name':
            self.name = str(value)
        elif key is 'x':
            self.coodinate[0] = float(value)
        elif key is 'y':
            self.coodinate[1] = float(value)
        elif key is 'z':
            self.coodinate[2] = float(value)
        elif key in ('m', 'M'):
            self.magmom = float(value)
        elif key in ('b', 'B'):
            self.belong = str(value)
        else:
            raise IndexError
        return None

    def __getitem__(self, key):
        if key is 'coodinate':
            return self.coodinate
        elif key is 'TF':
            tmp = list(self.TF)
            tmp2 = []
            for t in tmp:
                if t is True:
                    tmp2.append('T')
                else:
                    tmp2.append('F')
            return tmp2

        elif key is 'name':
            return self.name
        elif key is 'x':
            return self.coodinate[0]
        elif key is 'y':
            return self.coodinate[1]
        elif key is 'z':
            return self.coodinate[2]
        elif key is 'm':
            return self.magmom
        elif key is 'b':
            return self.belong
        elif key is None:
            return None
        else:
            raise IndexError
        return None

    def __neg__(self):
        ret = Atom(self)
        ret.coodinate = -(ret.coodinate)
        return ret

    def __add__(self, other):
        ret = Atom(self)
        if type(other) in [list, tuple, np.ndarray]:
            ret.coodinate += other
        elif type(other) is Atom:
            ret.coodinate += other.coodinate
        return ret

    def __sub__(self, other):
        if type(other) in [tuple, list]:
            other = np.array(other, float)
        return self + (-other)

    def transformed(self, matrix):
        ret = Atom(self)
        if type(matrix) in [list, tuple]:
            matrix = np.array(matrix, float)
        ret.coodinate = np.dot(matrix, ret.coodinate)
        return ret

    def distance(self, other):
        vec = self.coodinate - other.coodinate
        return np.linalg.norm(vec)

    def __iadd__(self, other):
        self.coodinate = (self + other).coodinate

    def __isub__(self, other):
        self.coodinate = (self - other).coodinate

    def transform(self, matrix):
        self.coodinate = self.transformed(matrix).coodinate

# a = Atom('Au', (1, 1, 1), (True,True,True))
# print(type(a))
# b = Atom(a)
# for k, v in b.__dict__.items():
#     print(k,v)
# A = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
# c = b.transform(A)
# print(c.coodinate)
# print(c.distance(a)**2)
