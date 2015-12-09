from info import Info
from poscar import Poscar
from incar import Incar
import copy

class Vaspm:

    def __init__(self, info=None):
        if info:
            self.info = info
        else:
            self.info = Info()
        self.poscar = Poscar(self.info)
        self.incar = Incar(self.info)

    def read_poscar(self, adress):
        self.poscar.read(adress)
        print(self.info.elements)

    def write_poscar(self, adress):
        self.poscar.write(adress)

    def read_incar(self, adress):
        self.incar.read(adress)

    def write_incar(self, adress):
        self.incar.write(adress)

    def translation(self, vector):
        self.info.atoms.translation(vector)

    def transform(self, matrix):
        self.info.atoms.transform(matrix)

    def set_magmom_pos_to_in(self):
        self.info.set_magmom_pos_to_in()

    def set_magmom_in_to_pos(self):
        self.info.set_magmom_in_to_pos()

    def __add__(self, other):
        ret = Vaspm()
        ret.info = self.info + other.info
        ret.incar = Incar(ret.info)
        ret.poscar = Poscar(ret.info)
        return ret

    def split(self):
        infos = self.info.split()
        lis = []
        for info in infos.values():
            lis.append(Vaspm(info))
        return lis

    def set_belong(self, name=None):
        if name == None:
            self.info.atoms.set_belong(self.info.info['SYSTEM'])
        else:
            self.info.atoms.set_belong(name)

a = Vaspm()
a.read_poscar('POSCAR')
a.read_incar('INCAR')
a.set_belong()
a.set_magmom_in_to_pos()
a.write_poscar('POSCAR2')
