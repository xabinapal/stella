# -*- coding: utf-8 -*-

from stella.core.utils import CharStream, RewindableIterator

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

class RewindableIteratorTest(unittest.TestCase):
    def _get_rewindable_iterator(self):
        stream = io.StringIO('Hello World')
        charstream = CharStream(stream)
        rewindable_iterator = RewindableIterator(charstream)
        return rewindable_iterator

    def _test_rewindable_iterator(self, rewindable_iterator, value):
        fullread = ''.join(x for x in rewindable_iterator)
        self.assertEqual(fullread, value)
        with self.assertRaises(StopIteration):
            next(rewindable_iterator)

    def _test_length_rewindable_iterator(self, rewindable_iterator, value):
        fullread = ''.join(next(rewindable_iterator) for _ in range(len(value)))
        self.assertEqual(fullread, value)

    def _test_peek_rewindable_iterator(self, rewindable_iterator):
        peek = rewindable_iterator.peek()
        for x in rewindable_iterator:
            self.assertEqual(peek, x)
            try:
                peek = rewindable_iterator.peek()
            except:
                with self.assertRaises(StopIteration):
                    next(rewindable_iterator)

    def test_full_read(self):
        rewindable_iterator = self._get_rewindable_iterator()
        self._test_rewindable_iterator(rewindable_iterator, 'Hello World')

    def test_full_rewind(self):
        rewindable_iterator = self._get_rewindable_iterator()
        self._test_rewindable_iterator(rewindable_iterator, 'Hello World')
        rewindable_iterator.rewind()
        self._test_rewindable_iterator(rewindable_iterator, 'Hello World')

    def test_half_rewind(self):
        rewindable_iterator = self._get_rewindable_iterator()
        self._test_length_rewindable_iterator(rewindable_iterator, 'Hello ')
        rewindable_iterator.rewind()
        self._test_rewindable_iterator(rewindable_iterator, 'Hello World')

    def test_half_commit(self):
        rewindable_iterator = self._get_rewindable_iterator()
        self._test_length_rewindable_iterator(rewindable_iterator, 'Hello ')
        rewindable_iterator.commit()
        rewindable_iterator.rewind()
        self._test_rewindable_iterator(rewindable_iterator, 'World')

    def test_peek(self):
        rewindable_iterator = self._get_rewindable_iterator()
        self._test_peek_rewindable_iterator(rewindable_iterator)

    def test_peek_rewind(self):
        rewindable_iterator = self._get_rewindable_iterator()
        self._test_peek_rewindable_iterator(rewindable_iterator)
        rewindable_iterator.rewind()
        self._test_peek_rewindable_iterator(rewindable_iterator)
