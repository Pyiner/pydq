# -*- coding: utf-8 -*-
import six

__title__ = 'requests'
__version__ = '0.0.1'
__author__ = 'Pyiner'
__license__ = 'Apache 2.0'
__copyright__ = 'Copyright 2015 Pyiner'

__all__ = ['DataQuery']


class DataQuery(object):
    def __init__(self, data):
        self.data = data

    @staticmethod
    def item_exist(item, **kwargs):
        exist = True
        for k, v in kwargs.items():
            if k not in item or item[k] != v:
                exist = False
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

    def exclude(self, **kwargs):
        return self.query(False, **kwargs)

    def order_by(self, field):
        desc = field.startswith('-')
        field = field.strip('-')
        d = sorted(self.data, key=lambda x: x[field], reverse=desc)
        return self.__class__(data=d)

    def __iter__(self):
        return self.data

    def __getitem__(self, k):
        if not isinstance(k, (slice,) + six.integer_types):
            raise TypeError

        data = self.data
        if isinstance(k, slice):
            return data[k.start:k.stop:k.step]

        return data[k]


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
    }]

    dq = DataQuery(xdata)
    for i in dq.filter(c=1):
        print i
