import numpy as np
import copy


class Atom:

    # str and Atom are allowed as atom
    def __init__(self, atom=None, coordinate=None, TF=None, magmom=0, belong=None):
        self._name = None
        self._coordinate = np.array([0.0, 0.0, 0.0])
        self._TF = np.array([True, True, True])
        self._magmom = 0
        self._belong = None
        self._comment = None
        self._augsum = None
        self._augdif = None
        self._chgn = None
        self._pdos = None
        if atom:
            if isinstance(atom, str):
                self.name = atom
            elif type(atom) is Atom:
                self.__dict__ = copy.deepcopy(atom.__dict__)
            else:
                raise TypeError('atom must be Atom or str')
        if coordinate:
            self.coordinate = np.array(coordinate, float)
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
    def coordinate(self):
        return self._coordinate

    @coordinate.setter
    def coordinate(self, coordinate):
        if isinstance(coordinate, (list, tuple, np.ndarray)):
            self._coordinate = np.array(coordinate, float)
        else:
            raise TypeError('coordinate must be an iterable')

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

    @property
    def augsum(self):
        return self._augsum

    @augsum.setter
    def augsum(self, augmentation):
        if augmentation is not None:
            self._augsum = np.array(augmentation)
        else:
            self._augsum = None

    @property
    def augdif(self):
        return self._augdif

    @augdif.setter
    def augdif(self, augmentation):
        if augmentation is not None:
            self._augdif = np.array(augmentation)
        else:
            self._augdif = None

    @property
    def chgn(self):
        return self._chgn

    @chgn.setter
    def chgn(self, chgn):
        self._chgn = float(chgn)

    def __setitem__(self, key, value):
        if key is 'coordinate':
            self.coordinate = np.array(value, dtype=float)
        elif key is 'TF':
            self.TF = value
        elif key is 'name':
            self.name = str(value)
        elif key is 'x':
            self.coordinate[0] = float(value)
        elif key is 'y':
            self.coordinate[1] = float(value)
        elif key is 'z':
            self.coordinate[2] = float(value)
        elif key in ('m', 'M'):
            self.magmom = float(value)
        elif key in ('b', 'B'):
            self.belong = str(value)
        else:
            raise IndexError
        return None

    def __getitem__(self, key):
        if key is 'coordinate':
            return self.coordinate
        elif key is 'TF':
            return self.TF
        elif key is 'name':
            return self.name
        elif key is 'x':
            return self.coordinate[0]
        elif key is 'y':
            return self.coordinate[1]
        elif key is 'z':
            return self.coordinate[2]
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
        ret.coordinate = -(ret.coordinate)
        return ret

    def __add__(self, other):
        ret = Atom(self)
        if type(other) in [list, tuple, np.ndarray]:
            ret.coordinate += np.array(other)
        elif type(other) is Atom:
            ret.coordinate += other.coordinate
        return ret

    def __sub__(self, other):
        if type(other) in [tuple, list]:
            other = np.array(other, float)
        return self + (-other)

    def transformed(self, matrix):
        ret = Atom(self)
        if type(matrix) in [list, tuple]:
            matrix = np.matrix(matrix, float)
        ret.coordinate = np.dot(matrix, ret.coordinate)
        ret.coordinate = ret.coordinate[0]
        return ret

    def distance(self, other):
        vec = self.coordinate - other.coordinate
        return np.linalg.norm(vec)

    def __iadd__(self, other):
        self.coordinate = (self + other).coordinate

    def __isub__(self, other):
        self.coordinate = (self - other).coordinate

    def translation(self, vector):
        self.coordinate += vector

    def transform(self, matrix):
        self.coordinate = self.transformed(matrix).coordinate

    def rotation(self, axis, center, theta=None):
        'Rodrigues\'s formula'
        assert len(axis) == 3, 'vector must be 3dimension'
        assert len(center) == 3, 'vector must be 3dimension'
        vec = np.array(axis)
        cen = np.array(center)
        # vec = vec - cen
        if theta is None:
            theta = np.linalg.norm(vec)
        else:
            vec = vec * theta / np.linalg.norm(vec)
        vx = vec[0]
        vy = vec[1]
        vz = vec[2]
        I = np.matrix(np.identity(3))
        R = np.matrix((
            (0, -vz, vy),
            (vz, 0, -vx),
            (-vy, vx, 0)))
        M = I + R * np.sin(theta) / theta + R.dot(R) * (1-np.cos(theta)) / (theta**2)
        self.coordinate -= cen
        self.transform(M)
        self.coordinate += cen

    def cartesianyzation(self, lattice):
        tmp = np.array([0., 0., 0.])
        for i in range(3):
            tmp += lattice[i] * self.coordinate[i]
        self.coordinate = tmp

# a = Atom('Au', (1, 1, 1), (False, True, True))
# print(a.TF)
# print(type(a))
# b = Atom(a)
# for k, v in b.__dict__.items():
#     print(k,v)
# A = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
# c = b.transform(A)
# print(c.coordinate)
# print(c.distance(a)**2)
