from .frw import Frw
from .tag import Tag
import re


class Chgcar(Frw):
    def cast_line(self, line):
        ret = line.strip()
        ret = re.split('\s+', ret)
        return ret

    def read(self, adress):
        self.start_reading(adress)
        self.info.tag['SYSTEM'] = Tag('SYSTEM', self.nextline)
