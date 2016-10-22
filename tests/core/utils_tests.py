# -*- coding: utf-8 -*-

from stella.core.utils import CharStream, Rewinder

import io
import unittest

class CharStreamTest(unittest.TestCase):
    def _test_charstream(self, stream, value):
        charstream = CharStream(stream)
        self.assertEqual(''.join(c for c in charstream), value)

    def test_ascii_bytes(self):
        stream = b'Hello World'
        self._test_charstream(stream, 'Hello World')

    def test_ascii_str(self):
        stream = 'Hello World'
        self._test_charstream(stream, 'Hello World')

    def test_ascii_bytesio(self):
        stream = io.BytesIO(b'Hello World')
        self._test_charstream(stream, 'Hello World')

    def test_ascii_stringio(self):
        stream = io.StringIO('Hello World')
        self._test_charstream(stream, 'Hello World')

    def test_unicode_bytes(self):
        stream = b'\xe2\xac\x86Hello\xe2\xac\x87'
        self._test_charstream(stream, '⬆Hello⬇')

    def test_unicode_str(self):
        stream = '⬆World⬇'
        self._test_charstream(stream, '⬆World⬇')

    def test_unicode_bytesio(self):
        stream = io.BytesIO(b'\xe2\xac\x86Hello\xe2\xac\x87')
        self._test_charstream(stream, '⬆Hello⬇')

    def test_unicode_stringio(self):
        stream = io.StringIO('⬆World⬇')
        self._test_charstream(stream, '⬆World⬇')

class RewinderTest(unittest.TestCase):
    def _get_rewinder(self):
        stream = io.StringIO('Hello World')
        charstream = CharStream(stream)
        rewinder = Rewinder(charstream)
        return rewinder

    def _test_rewinder(self, rewinder, value):
        fullread = ''.join(x for x in rewinder)
        self.assertEqual(fullread, value)
        with self.assertRaises(StopIteration):
            next(rewinder)

    def _test_length_rewinder(self, rewinder, value):
        fullread = ''.join(next(rewinder) for _ in range(len(value)))
        self.assertEqual(fullread, value)

    def _test_peek_rewinder(self, rewinder):
        peek = rewinder.peek()
        for x in rewinder:
            self.assertEqual(peek, x)
            try:
                peek = rewinder.peek()
            except:
                with self.assertRaises(StopIteration):
                    next(rewinder)

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

    def test_peek(self):
        rewinder = self._get_rewinder()
        self._test_peek_rewinder(rewinder)

    def test_peekrewind(self):
        rewinder = self._get_rewinder()
        self._test_peek_rewinder(rewinder)
        rewinder.rewind()
        self._test_peek_rewinder(rewinder)
