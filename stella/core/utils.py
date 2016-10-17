# -*- coding: utf-8 -*-

import io
import collections

################################################################################
### CharStream
################################################################################

class CharStream(object):
    def __init__(self, stream, encoding='utf-8'):
        self.stream = stream
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
        c = self.stream.read(1)
        if not c:
            raise StopIteration

        return c

################################################################################
### Rewinder
################################################################################

class Rewinder(object):
    def __init__(self, iterator):
        self.iterator = iterator
        self.buffer = collections.deque()
        self.buf_pos = 0
        self.buf_read = False

    def __iter__(self):
        return self

    def __next__(self):
        n = self.peek()
        if self.buf_read and self.buf_pos >= len(self.buffer):
            self.buf_read = False

        self.buf_pos += 1
        return n

    def peek(self):
        if self.buf_read and self.buf_pos < len(self.buffer):
            n = self.buffer[self.buf_pos]
        else:
            n = next(self.iterator)
            self.buffer.append(n)
            self.buf_read = True
        
        return n

    def rewind(self):
        self.buf_pos = 0
        self.buf_read = True

    def commit(self):
        for _ in range(self.buf_pos):
            self.buffer.popleft()

        self.buf_pos = 0
        self.buf_read = len(self.buffer) != 0
