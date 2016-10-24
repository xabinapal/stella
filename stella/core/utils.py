# -*- coding: utf-8 -*-

import io
import abc

__all__ = ['CharStream', 'RewindableIterator']

bytes_iterator = type(iter(b''))
str_iterator = type(iter(''))

################################################################################
### CharStream
################################################################################

class CharStream(object):
    def __init__(self, stream, encoding='utf-8'):
        self.stream = iter(stream) if type(stream) in (str, bytes) else stream
        self.encoding = encoding

    def __iter__(self):
        return self

    def __next__(self):
        c = self._read()
        is_str = isinstance(c, str)
        while not is_str:
            try:
                c = str(c, self.encoding)
                is_str = True
            except UnicodeDecodeError as ude:
                try:
                    c += self._read()
                except StopIteration:
                    raise ude
        return c

    def _read(self):
        if type(self.stream) == bytes_iterator:
            return bytes([next(self.stream)])
        if type(self.stream) == str_iterator:
            return next(self.stream)

        c = self.stream.read(1)
        if not c:
            raise StopIteration

        return c

################################################################################
### RewindableIteratorBase
################################################################################
class RewindableIteratorBase(metaclass=abc.ABCMeta):
    def __init__(self, iterator):
        self.iterator = iterator
        self.buffer = []
        self.buf_pos = {}
        self.next_instance_id = 0

    def _create_instance(self):
        instance_id = self.next_instance_id
        self.next_instance_id += 1
        self.buf_pos[instance_id] = 0
        return instance_id

    def _clone_instance(self, instance_id):
        new_instance_id = self._create_instance()
        self.buf_pos[new_instance_id] = self.buf_pos[instance_id]
        return new_instance_id

    def _next(self, instance_id):
        n = self._peek(instance_id)
        self.buf_pos[instance_id] += 1
        return n

    def _peek(self, instance_id):
        if self.buf_pos[instance_id] < len(self.buffer):
            n = self.buffer[self.buf_pos[instance_id]]
        else:
            n = next(self.iterator)
            self.buffer.append(n)

        return n

    def _rewind(self, instance_id):
        self.buf_pos[instance_id] = 0

    def _commit(self, instance_id):
        min_pos = self.buf_pos[instance_id]
        for x in self.buf_pos.values():
            if min_pos > x:
                min_pos = x

        for x in self.buf_pos:
            self.buf_pos[x] -= min_pos

        del self.buffer[:min_pos]

################################################################################
### RewindableIterator
################################################################################

class RewindableIterator(object):
    def __init__(self, *args):
        if isinstance(args[0], RewindableIteratorBase):
            self.base = args[0]
            self.instance_id = self.base._clone_instance(args[1])
        else:
            iterator = args[0]
            self.base = RewindableIteratorBase(iterator)
            self.instance_id = self.base._create_instance()

    def __iter__(self):
        return self

    def __next__(self):
        return self.base._next(self.instance_id)

    def peek(self):
        return self.base._peek(self.instance_id)

    def rewind(self):
        return self.base._rewind(self.instance_id)

    def commit(self):
        return self.base._commit(self.instance_id)

    def clone(self):
        return self.__class__(self.base, self.instance_id)
