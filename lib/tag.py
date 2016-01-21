import re


class Tag:

    def __init__(self, key="", val=""):
        self._comment_out = False
        self._key = key
        self._val = val
        self._comment = None

    def readline_incar(self, line):
        if not isinstance(line, str):
            raise TypeError('readline_incar\'s argument must be str')
        line = line.strip()
        if line[0] in ('!'):
            self._comment_out = True
            line = line[1:]
        if '!' in line:
            line, self._comment = line.split('!', 1)
        if '=' in line:
            self._key, self._val = line.split('=', 1)
            self._key = self._key.strip()
            self._val = self._val.strip()
        else:
            raise RuntimeError('%s has no value' % line)

    def strline_incar(self):
        ret = ''
        if self.comment_out == True:
            ret += '! '
        ret += self.key
        ret += ' = '
        ret += self.val
        if self.comment:
            ret += ' !' + self.comment
        return ret

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, key):
        self._key = key

    @property
    def val(self):
        return self._val

    @val.setter
    def val(self, val):
        self._val = val

    @property
    def comment_out(self):
        return self._comment_out

    @comment_out.setter
    def comment_out(self, comment_out):
        self._comment_out = comment_out

    @property
    def comment(self):
        return self._comment

    @comment.setter
    def comment(self, comment):
        self._comment = comment

# a = '!aa=b !a'
# b = Tag()
# b.readline_incar(a)
# print(b.key)
# print(b.strline_incar())
