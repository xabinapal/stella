# -*- coding: utf-8 -*-

import io
import unittest

from stella.core.utils import CharStream, Rewinder

class CharStreamTest(unittest.TestCase):
    def _test_charstream(self, stream, value):
        charstream = CharStream(stream)
        self.assertEqual(''.join(c for c in charstream), value)

    def test_ascii_bytesio(self):
        stream = io.BytesIO(b'Hello World')
        self._test_charstream(stream, 'Hello World')

    def test_unicode_bytesio(self):
        stream = io.BytesIO(b'H\xe2\xac\x86e\xe2\x9e\xa1l\xe2\xac\x87l\xe2\xac\x85o')
        self._test_charstream(stream, 'H⬆e➡l⬇l⬅o')

    def test_ascii_stringio(self):
        stream = io.StringIO('Hello World')
        self._test_charstream(stream, 'Hello World')

    def test_unicode_stringio(self):
        stream = io.StringIO('W⬆o➡r⬇l⬅d')
        self._test_charstream(stream, 'W⬆o➡r⬇l⬅d')

class RewinderTest(unittest.TestCase):
    def _get_rewinder(self):
        stream = io.StringIO('Hello World')
        charstream = CharStream(stream)
        rewinder = Rewinder(charstream)
        return rewinder

    def _test_rewinder(self, rewinder, value):
        fullread = ''.join(x for x in rewinder)
        self.assertEqual(fullread, value)

    def _test_length_rewinder(self, rewinder, value):
        fullread = ''.join(next(rewinder) for _ in range(len(value)))
        self.assertEqual(fullread, value)

    def test_fullread(self):
        rewinder = self._get_rewinder()
        self._test_rewinder(rewinder, 'Hello World')

    def test_fullrewind(self):
        rewinder = self._get_rewinder()
        self._test_rewinder(rewinder, 'Hello World')
        rewinder.rewind()
        self._test_rewinder(rewinder, 'Hello World')

    def test_halfrewind(self):
        rewinder = self._get_rewinder()
        self._test_length_rewinder(rewinder, 'Hello ')
        rewinder.rewind()
        self._test_rewinder(rewinder, 'Hello World')

    def test_halfcommit(self):
        rewinder = self._get_rewinder()
        self._test_length_rewinder(rewinder, 'Hello ')
        rewinder.commit()
        rewinder.rewind()
        self._test_rewinder(rewinder, 'World')
