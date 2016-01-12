import numpy as np
import copy


class Atom:

    # str and Atom are allowed as atom
    def __init__(self, atom=None, coodinate=None, TF=None, magmom=0, belong=None):
        self._name = None
        self._coodinate = np.array([0.0, 0.0, 0.0])
        self._TF = np.array([True, True, True])
        self._magmom = 0
        self._belong = None
        self._comment = None
        self._pdos = None
        if atom:
            if isinstance(atom, str):
                self.name = atom
            elif type(atom) is Atom:
                self.__dict__ = copy.deepcopy(atom.__dict__)
            else:
                raise TypeError('atom must be Atom or str')
        if coodinate:
            self.coodinate = np.array(coodinate, float)
        if TF:
            self.TF = np.array(TF, bool)
        if magmom:
            self.magmom = magmom
        if belong:
            if type(belong) in (int, float, str):
                self.belong = str(belong)
            else:
                raise TypeError
        # return None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = str(name)

    @property
    def coodinate(self):
        return self._coodinate

    @coodinate.setter
    def coodinate(self, coodinate):
        if isinstance(coodinate, (list, tuple, np.ndarray)):
            self._coodinate = np.array(coodinate, float)
        else:
            raise TypeError('coodinate must be an iterable')

    @property
    def TF(self):
        return ['T' if x else 'F' for x in self._TF]

    @TF.setter
    def TF(self, TF):
        if not isinstance(TF, (list, tuple, np.ndarray)):
            raise TypeError('TF must be an iterable')
        elif len(TF) is not 3:
            raise IndexError('TF must have 3 values')
        else:
            for i in range(3):
                if TF[i] in ('F', 'f', False):
                    self._TF[i] = False
                else:
                    self._TF[i] = True

    @property
    def magmom(self):
        return self._magmom

    @magmom.setter
    def magmom(self, magmom):
        if isinstance(magmom, (int, float, str)):
            self._magmom = float(magmom)
        elif magmom is None:
            self._magmom = None
        else:
            raise TypeError('magmom`s argument must be int or float')

    @property
    def belong(self):
        return self._belong

    @belong.setter
    def belong(self, belong):
        if belong is not None:
            self._belong = str(belong)
        else:
            self._belong = None

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        if comment is not None:
            self._comment = str(comment)
        else:
            self._comment = None

    def __setitem__(self, key, value):
        if key is 'coodinate':
            self.coodinate = np.array(value, dtype=float)
        elif key is 'TF':
            self.TF = value
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
            ret.coodinate += np.array(other)
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
            matrix = np.matrix(matrix, float)
        ret.coodinate = np.dot(matrix, ret.coodinate)
        ret.coodinate = ret.coodinate[0]
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

# a = Atom('Au', (1, 1, 1), (False, True, True))
# print(a.TF)
# print(type(a))
# b = Atom(a)
# for k, v in b.__dict__.items():
#     print(k,v)
# A = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
# c = b.transform(A)
# print(c.coodinate)
# print(c.distance(a)**2)
