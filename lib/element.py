class Element:

    def __init__(self, element=None, num=None, LUAUL=None, LUAUU=None, LUAUJ=None):
        self.name = ''
        self.num = 0
        self.LUAUL = None
        self.LUAUU = None
        self.LUAUJ = None
        if element:
            if type(element) == Element:
                self.name = element.name
                self.num = element.num
                self.LUAUJ = element.LUAUJ
                self.LUAUL = element.LUAUL
                self.LUAUU = element.LUAUU
            if type(element) == str:
                self.name = element
            else:
                raise TypeError
        if num:
            if type(num) in (int, str):
                self.num = int(num)
            else:
                raise TypeError
        if LUAUJ:
            if type(LUAUJ) in (int, float):
                self.LUAUJ = LUAUJ
            else:
                raise TypeError
        if LUAUU:
            if type(LUAUU) in (int, float):
                self.LUAUU = LUAUU
            else:
                raise TypeError
        if LUAUL:
            if type(LUAUL) in (int, float):
                self.LUAUL = LUAUL
            else:
                raise TypeError

    def set_num(self, num):
        self.num = int(num)

    def set_name(self, name):
        self.name = str(name)

    def set_LUAUL(self, LUAUL):
        self.LUAUL = float(LUAUL)

    def set_LUAUU(self, LUAUU):
        self.LUAUU = float(LUAUU)

    def set_LUAUJ(self, LUAUJ):
        self.LUAUJ = float(LUAUJ)
