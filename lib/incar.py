import re
from .frw import Frw
from .tag import Tag


class Incar(Frw):

    def read(self, adress):
        for line in open(adress):
            cast = line.strip()
            if cast == '':
                self.info.tags[Tag()] = Tag()
                self.info.tags.setTag(Tag(), Tag())
            else:
                self.info.tags.setTagFromIncarLine(cast)
                # tag = Tag()
                # tag.readline_incar(cast)
                # self.info.tags[tag.key] = tag

        # self.start_reading(adress)
        # line = self.nextline()
        # while line:
        #     self.info.incar[line[0]] = line[1]
        #     line = self.nextline()
        # self.end_reading()

    def write(self, adress):
        f = open(adress, 'w')
        for key, val in self.info.tags.items():
            if isinstance(key, Tag):
                f.write('\n')
            else:
                f.write(val.strline_incar() + '\n')
        # for key in self.info.incar:
        #     if key != '':
        #         f.write(key + '=' + self.info.incar[key] + '\n')
        f.close()

    def cast_line(self, line):
        # line = line.strip()
        # if '=' in line:
        #     line = line.split('=', 1)
        #     line = list(map(lambda x: x.strip(), line))
        # else:
        #     line = [line, '']
        return line
