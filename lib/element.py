class Element:

    def __init__(self, element=None, num=None, LDAUL=None, LDAUU=None, LDAUJ=None):
        self._name = ''
        self._num = 0
        self._LDAUL = -1
        self._LDAUU = 0.0
        self._LDAUJ = 0.0
        if element:
            if isinstance(element, Element):
                self.name = element.name
                self.num = element.num
                self.LDAUJ = element.LDAUJ
                self.LDAUL = element.LDAUL
                self.LDAUU = element.LDAUU
            elif isinstance(element, str):
                self.name = element
            else:
                print(element.name)
                raise TypeError
        if num:
            if type(num) in (int, str):
                self.num = int(num)
            else:
                raise TypeError
        if LDAUJ:
            if type(LDAUJ) in (int, float):
                self.LDAUJ = LDAUJ
            else:
                raise TypeError
        if LDAUU:
            if type(LDAUU) in (int, float):
                self.LDAUU = LDAUU
            else:
                raise TypeError
        if LDAUL:
            if type(LDAUL) in (int, float):
                self.LDAUL = LDAUL
            else:
                raise TypeError

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = str(name)

    @property
    def num(self):
        return self._num

    @num.setter
    def num(self, num):
        self._num = int(num)

    @property
    def LDAUL(self):
        return self._LDAUL

    @LDAUL.setter
    def LDAUL(self, LDAUL):
        self._LDAUL = int(LDAUL)

    @property
    def LDAUU(self):
        return self._LDAUU

    @LDAUU.setter
    def LDAUU(self, LDAUU):
        self._LDAUU = float(LDAUU)

    @property
    def LDAUJ(self):
        return self._LDAUJ

    @LDAUJ.setter
    def LDAUJ(self, LDAUJ):
        self._LDAUJ = float(LDAUJ)

    # def set_num(self, num):
    #     self.num = int(num)
    #
    # def set_name(self, name):
    #     self.name = str(name)
    #
    # def set_LDAUL(self, LDAUL):
    #     self.LDAUL = float(LDAUL)
    #
    # def set_LDAUU(self, LDAUU):
    #     self.LDAUU = float(LDAUU)
    #
    # def set_LDAUJ(self, LDAUJ):
    #     self.LDAUJ = float(LDAUJ)
