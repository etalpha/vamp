from .tag import Tag
from collections import OrderedDict


class Tags:

    def __init__(self):
        self._tags = OrderedDict()

    def setTag(self, key, val):
        if not isinstance(key, (str, Tag)):
            raise TypeError('key must be str')
        if key in self._tags:
            self._tags[key].val = val
        else:
            self._tags[key] = Tag(key, val)

    def setTagFromIncarLine(self, line):
        new_tag = Tag()
        new_tag.readline_incar(line)
        self._tags[new_tag.key] = new_tag

    def getTag(self, key):
        return self._tags[key].val

    def tagExists(self, key):
        if key in self._tags:
            return True
        else:
            return False

    def commentOut(self, key):
        self._tags[key].comment_out = True

    def uncomment(self, key):
        self._tags[key].comment_out = False

    def items(self):
        return self._tags.items()


# a = Tag()
# a.key = 'a'
# a.val = 'b'
#
# cl = Tags()
# cl['a'] = a
# print(cl['a'].val)
# cl['a'] = 'aaa'
# print(cl['a'].val)
