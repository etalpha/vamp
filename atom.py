import numpy as np
import copy


class Atom:

    def __init__(self, name=None, coodinate=None, TF=None, magmom=0, belong=None):
        self.name = None
        self.coodinate = np.array([0.0, 0.0, 0.0])
        self.TF = np.array([True, True, True])
        self.magmom = None
        self.belong = None
        if type(name) is str:
            self.name = str(name)
        if type(name) is Atom:
            self.name = copy.deepcopy(name.name)
            self.coodinate = copy.deepcopy(name.coodinate)
            self.magmom = copy.deepcopy(name.magmom)
            self.belong = copy.deepcopy(name.belong)
        if coodinate:
            self.coodinate = np.array(coodinate, float)
        if TF:
            self.TF = np.array(TF, bool)
        if magmom:
            self.magmom = magmom
        if belong:
            self.belong = belong
        return None

    def __setitem__(self, key, value):
        if key is 'coodinate':
            self.coodinate = np.array(value, dtype=float)
        elif key is 'TF':
            self.TF = np.array(value, dtype=bool)
            for i in range(3):
                if value[i] == 'F':
                    self.TF[i] = False
        elif key is 'name':
            self.name = value
        elif key is 'x':
            self.coodinate[0] = value
        elif key is 'y':
            self.coodinate[1] = value
        elif key is 'z':
            self.coodinate[2] = value
        elif key is 'm':
            self.magmom = float(value)
        elif key is 'b':
            self.belong = str(value)
        else:
            raise IndexError
        return None

    def __getitem__(self, key):
        if key is 'coodinate':
            return self.coodinate
        elif key is 'TF':
            return self.TF
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

    def transform(self, matrix):
        ret = Atom(self)
        if type(matrix) in [list, tuple]:
            matrix = np.array(matrix, float)
        ret.coodinate = np.dot(matrix, ret.coodinate)
        return ret

    def distance(self, other):
        vec = self.coodinate - other.coodinate
        return np.linalg.norm(vec)


# a = Atom('Au', (1, 1, 1))
# b = Atom(a, (1, 2, 3))
# A = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
# c = b.transform(A)
# print(c.coodinate)
# print(c.distance(a)**2)
