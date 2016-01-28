from .atoms import Atoms
from .atom import Atom
from .elements import Elements
from .element import Element
from .tag import Tag
import numpy as np
from collections import OrderedDict
import re
import copy


class Info:

    def __init__(self, info=None):
        self._atoms = Atoms()
        self._elements = Elements()
        self._scale = 0
        self._lattice = []
        self._selective_dynamics = False
        self._cartesian = False
        self._tags = OrderedDict()
        self._chgsum = None
        self._chgdif = None
        self._chgcell = None
        if info:
            if type(info) == Info:
                self.__dict__ = copy.deepcopy(info.__dict__)
            else:
                raise TypeError

    def add_atom(self, name, coordinate=(0, 0, 0), TF=(True, True, True), magmom=None, belong=None):
        self.atoms.append(Atom(name, coordinate, TF, magmom, belong))

    def add_element(self, name, num, LUAUL=None, LUAUU=None, LUAUJ=None):
        self.elements[name] = Element(name, num, LUAUL, LUAUU, LUAUJ)

    def create_elements(self):
        self.elements = self.atoms.create_elements()

    def set_magmom_pos_to_in(self):
        lis = []
        for atom in self.atoms:
            lis.append(atom['m'])
        lis2 = []
        lis2.append([0, lis[0]])
        for mag in lis:
            if lis2[-1][1] == mag:
                lis2[-1][0] += 1
            else:
                lis2.append([1, mag])
        lis3 = []
        for item in lis2:
            lis3.append('*'.join(map(str, item)))
        self.tags['MAGMOM'].val = ' '.join(lis3)

    def set_magmom_in_to_pos(self):
        if 'MAGMOM' in self.tags:
            mag = self.tags['MAGMOM'].val
            mags = re.split('\s+', mag)
            for i in range(len(mags)):
                if '*' in mags[i]:
                    mags[i] = mags[i].split('*')
                else:
                    mags[i] = ['1', mags[i]]
            lis = []
            for mag in mags:
                for i in range(int(mag[0])):
                    lis.append(mag[1])
            if len(lis) != len(self.atoms):
                raise RuntimeError('the number of magmom is not consistent')
            for mag, atom in zip(lis, self.atoms):
                atom.magmom = mag

    def set_LDAU_tag_to_elem(self):
        if 'LDAUL' not in self.tags:
            return self
        if 'LDAUU' not in self.tags:
            return self
        if 'LDAUJ' not in self.tags:
            return self
        LDAUL = list(map(float, re.split('\s+', self.tags['LDAUL'].val)))
        LDAUU = list(map(float, re.split('\s+', self.tags['LDAUU'].val)))
        LDAUJ = list(map(float, re.split('\s+', self.tags['LDAUJ'].val)))
        if len(LDAUL) != len(LDAUU) or len(LDAUU) != len(LDAUJ):
            raise RuntimeError(
                'the number of LDAU is not consistent with POSCAR')
        if len(LDAUL) != len(self.elements):
            print(len(LDAUL))
            print(len(self.elements))
            raise RuntimeError(
                'the number of LDAU is not consistent with POSCAR')
        for ldaul, ldauu, ldauj, element in zip(LDAUL, LDAUU, LDAUJ, self.elements.values()):
            element.LDAUL = ldaul
            element.LDAUU = ldauu
            element.LDAUJ = ldauj

    def set_LDAU_elem_to_tag(self):
        ldaul = []
        ldauu = []
        ldauj = []
        for element in self.elements.values():
            ldaul.append(str(element.LDAUL))
            ldauu.append(str(element.LDAUU))
            ldauj.append(str(element.LDAUJ))
        self.tags['LDAUL'].val = ' '.join(ldaul)
        self.tags['LDAUU'].val = ' '.join(ldauu)
        self.tags['LDAUJ'].val = ' '.join(ldauj)

    def __add__(self, other):
        ret = copy.deepcopy(self)
        ret.atoms.merge(other.atoms)
        ret.elements.merge(other.elements)
        if ret.chgsum is not None and other.chgsum is not None:
            ret.chgsum += other.chgsum
        elif other.chgsum is not None:
            ret.chgsum = other.chgsum
        if ret.chgdif is not None and other.chgdif is not None:
            ret.chgdif += other.chgdif
        elif other.chgdif is not None:
            ret.chgdif = other.chgdif
        for atom in ret.atoms:
            if atom.augdif is None and atom.augsum is not None:
                atom.augdif = atom.augsum[:]
                for i in range(len(atom.augdif)):
                    atom.augdif[i] = '0.0'
        return ret

    def split(self):
        'This method returns splited dictionaty as info type'
        if 'MAGMOM' in self.tags:
            self.set_magmom_in_to_pos()
        if 'LDAUJ' in self.tags:
            self.set_LDAU_tag_to_elem()
        infos = dict()
        for atom in self.atoms:
            if atom.belong not in infos.keys():
                infos[atom.belong] = copy.deepcopy(self)
                infos[atom.belong].atoms = Atoms()
            infos[atom.belong].atoms.append(Atom(atom))
        if 'MAGMOM' in self.tags:
            self.set_magmom_pos_to_in()
        if 'LDAUJ' in self.tags:
            self.set_LDAU_elem_to_tag()
        return infos

    def cartesianyzation(self):
        if self.cartesian == True:
            return self
        else:
            self.atoms.cartesianyzation(self.lattice)
            self.cartesian = True

    def reverse_mag(self):
        self.set_magmom_in_to_pos()
        self.set_LDAU_tag_to_elem()
        self.atoms.reverse_mag()
        self.set_magmom_pos_to_in()
        self.set_LDAU_elem_to_tag()

    @property
    def atoms(self):
        return self._atoms

    @atoms.setter
    def atoms(self, atoms):
        self._atoms = atoms

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        self._elements = elements

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, scale):
        self._scale = scale

    @property
    def lattice(self):
        return self._lattice

    @lattice.setter
    def lattice(self, lattice):
        self._lattice = lattice

    @property
    def selective_dynamics(self):
        return self._selective_dynamics

    @selective_dynamics.setter
    def selective_dynamics(self, selective_dynamics):
        self._selective_dynamics = selective_dynamics

    @property
    def cartesian(self):
        return self._cartesian

    @cartesian.setter
    def cartesian(self, cartesian):
        if type(cartesian) == bool:
            self._cartesian = cartesian
        elif isinstance(cartesian, str):
            if cartesian[0] in ('c', 'C'):
                self._cartesian = True
            else:
                self._cartesian = False
        else:
            raise TypeError

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, tags):
        self._tags = tags

    @property
    def chgsum(self):
        return self._chgsum

    @chgsum.setter
    def chgsum(self, chgsum):
        self._chgsum = np.array(chgsum)

    @property
    def chgdif(self):
        return self._chgdif

    @chgdif.setter
    def chgdif(self, chgdif):
        self._chgdif = np.array(chgdif)

    @property
    def chgcell(self):
        return self._chgcell

    @chgcell.setter
    def chgcell(self, chgcell):
        self._chgcell = chgcell
