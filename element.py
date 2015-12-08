class Element:

    def __init__(self, name=None):
        self.name = name
        self.num = 0
        self.LUAUL = None
        self.LUAUU = None
        self.LUAUJ = None

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
