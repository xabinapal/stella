# -*- coding: utf-8 -*-

import io
import unittest

from stella.core.utils import CharStream
from stella.core.interpreter import Token, Tokenizer, Lexer

from stella.core.grammar import Keywords, Tokens

class LexerTest(unittest.TestCase):
    tokens = [Token(x, x.name) for x in Keywords]
    tokenizer = Tokenizer(Tokens)

    def test_keywords(self):
        keywords = ' '.join((x.name for x in Keywords))
        stream = io.StringIO(keywords)
        lexer = lexer = Lexer(stream, self.tokenizer)
        results = [x for x in lexer if not repr(x.ttype).endswith('WHITESPACE')]
        self.assertEqual(self.tokens, results)

class ParserTest(unittest.TestCase):
    pass