from vaspm.lib.info import Info
from vaspm.lib.poscar import Poscar
from vaspm.lib.incar import Incar
from vaspm.lib.doscar import Doscar
from vaspm.lib.com import Com
import numpy as np
import os


class Vaspm:

    def __init__(self, info=None):
        if info:
            self.info = info
        else:
            self.info = Info()
        self._poscar = Poscar(self.info)
        self._incar = Incar(self.info)
        self._doscar = Doscar(self.info)
        self.com = Com(self.info)
        self.incar = self.info.tags
        self.atoms = self.info.atoms

    def read(self, adress):
        if not os.path.isdir(adress):
            raise RuntimeError('read argument must be directory')
        self.read_poscar(adress)
        self.read_incar(adress)

    def read_poscar(self, adress='POSCAR'):
        if os.path.isfile(adress):
            self._poscar.read(adress)
        elif os.path.isdir(adress):
            adress = os.path.join(adress, 'POSCAR')
            if os.path.isfile(adress):
                self._poscar.read(adress)
        else:
            print('Failed to read')

    def write_poscar(self, adress):
        if os.path.isdir(adress):
            adress = os.path.join(adress, 'POSCAR')
        self._poscar.write(adress)

    def read_incar(self, adress='INCAR'):
        if os.path.isfile(adress):
            self._incar.read(adress)
        elif os.path.isdir(adress):
            adress = os.path.join(adress, 'INCAR')
            if os.path.isfile(adress):
                self._incar.read(adress)
        else:
            print('Failed to read')

    def write_incar(self, adress):
        if os.path.isdir(adress):
            adress = os.path.join(adress, 'INCAR')
        self._incar.write(adress)

    def read_com(self, adress):
        self.com.read(adress)

    def read_PDOS(self, DOSCAR):
        self._doscar.read(DOSCAR)

    def translation(self, vector):
        'translation'
        self.info.atoms.translation(vector)

    def transform(self, matrix):
        'rotation'
        self.info.atoms.transform(matrix)

    def rotation(self, vector, theta=None):
        'Rodrigues\'s formula'
        assert len(vector) == 3, 'vector must be 3dimension'
        vec = np.array(vector)
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
        self.transform(M)

    def set_magmom_pos_to_in(self):
        self.info.set_magmom_pos_to_in()

    def set_magmom_in_to_pos(self):
        self.info.set_magmom_in_to_pos()

    def set_LDAU_tag_to_elem(self):
        self.info.set_LDAU_tag_to_elem()

    def set_LDAU_elem_to_tag(self):
        self.info.set_LDAU_elem_to_tag()

    def set_num(self):
        for num, atom in enumerate(self.atoms):
            atom.comment = atom.name + str(num + 1)

    def get_belonginfo(self, other):
        'get belonginfo from other'
        if len(self.atoms) != len(other.atoms):
            raise RuntimeError('number of atoms not consistant')
        for atom, otom in zip(self.atoms, other.atoms):
            atom.belong = other.belong

    def __add__(self, other):
        info = self.info + other.info
        ret = Vaspm(info)
        return ret

    def split(self):
        infos = self.info.split()
        print(infos)
        ret = dict()
        for bel, info in infos.items():
            ret[bel] = Vaspm(info)
        return ret

    def set_belong(self, name=None):
        if name is None:
            self.info.atoms.set_belong(self.info.incar['SYSTEM'])
        else:
            self.info.atoms.set_belong(name)
