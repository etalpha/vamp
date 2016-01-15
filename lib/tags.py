from .tag import Tag
from collections import OrderedDict


class Tags(OrderedDict):

    def __init__(self):
        OrderedDict.__init__(self)

    def __setitem__(self, key, val):
        if isinstance(val, Tag):
            OrderedDict.__setitem__(self, key, val)
        elif isinstance(val, str):
            # print(self[key])
            self[key].val = val


# a = Tag()
# a.key = 'a'
# a.val = 'b'
#
# cl = Tags()
# cl['a'] = a
# print(cl['a'].val)
# cl['a'] = 'aaa'
# print(cl['a'].val)
