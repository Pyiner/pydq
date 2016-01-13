# -*- coding: utf-8 -*-
import six

__title__ = 'pydq'
__version__ = '0.0.1'
__author__ = 'Pyiner'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015 Pyiner'

__all__ = ['DataQuery']

LOOKUP_SEP = '__'
LOOKUPS = ['exact', 'lt', 'lte', 'gt', 'gte']


class DataQuery(object):
    def __init__(self, data):
        self.data = data
        self.order_fields = []

    def field_check(self, item_value, lookup, value):
        if lookup == 'exact':
            return item_value == value
        elif lookup == 'lt':
            return item_value < value
        elif lookup == 'lte':
            return item_value <= value
        elif lookup == 'gt':
            return item_value > value
        elif lookup == 'gte':
            return item_value >= value
        return False

    def item_exist(self, item, **kwargs):
        exist = True
        for k, v in kwargs.items():
            names = k.split(LOOKUP_SEP)
            item_key = names[0]

            if item_key not in item:
                continue
            if len(names) == 2 and names[1] in LOOKUPS:
                lookup = names[1]
            else:
                lookup = 'exact'

            exist = self.field_check(item[item_key], lookup, v)

            if exist is False:
                break
        return exist

    def query(self, negate, **kwargs):
        d = []
        for item in self.data:
            exist = self.item_exist(item, **kwargs)
            if exist is negate:
                d.append(item)
        return self.__class__(data=d)

    def filter(self, **kwargs):
        return self.query(True, **kwargs)

    def between(self, ):
        pass

    def exclude(self, **kwargs):
        return self.query(False, **kwargs)

    def cmp(self, x, y):
        for field in self.order_fields:
            desc = -1 if field.startswith('-') else 1
            field = field.strip('-')
            if x[field] == y[field]:
                continue
            if x[field] < y[field]:
                return -desc
            else:
                return desc
        return 0

    def cmp_to_key(self, mycmp):
        class K(object):
            def __init__(self, obj, *args):
                self.obj = obj

            def __lt__(self, other):
                return mycmp(self.obj, other.obj) < 0

            def __gt__(self, other):
                return mycmp(self.obj, other.obj) > 0

            def __eq__(self, other):
                return mycmp(self.obj, other.obj) == 0

            def __le__(self, other):
                return mycmp(self.obj, other.obj) <= 0

            def __ge__(self, other):
                return mycmp(self.obj, other.obj) >= 0

            def __ne__(self, other):
                return mycmp(self.obj, other.obj) != 0

        return K

    def order_by(self, *args):
        self.order_fields = args
        d = sorted(self.data, key=self.cmp_to_key(self.cmp))
        return self.__class__(data=d)

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, k):
        if not isinstance(k, (slice,) + six.integer_types):
            raise TypeError

        data = self.data
        if isinstance(k, slice):
            return data[k.start:k.stop:k.step]

        return data[k]

    def __len__(self):
        return self.data.__len__()


if __name__ == '__main__':
    xdata = [{
        'a': 1,
        'b': 2,
        'c': 3
    }, {
        'a': 2,
        'b': 1,
        'c': 3
    }, {
        'a': 3,
        'b': 2,
        'c': 1
    }, {
        'a': 2,
        'b': 2,
        'c': 1
    }]

    dq = DataQuery(xdata)
    for i in dq.filter(a=2):
        print i
