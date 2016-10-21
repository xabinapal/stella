# -*- coding: utf-8 -*-

import io
import unittest

from stella.core.utils import CharStream
from stella.core.interpreter.lexer import Tokenizer, Lexer
from stella.core.interpreter.parser import Parser
from stella.core.grammar import Keywords, Tokens

class LexerTest(unittest.TestCase):
    tokenizer = Tokenizer(Tokens)

    def test_notoken(self):
        stream = io.StringIO('ñ')
        char_stream = CharStream(stream)
        lexer = lexer = Lexer(char_stream, self.__class__.tokenizer)
        self.assertIsNone(next(lexer).ttype)

    def test_keywords(self):
        stream = io.StringIO(' '.join((x.expr for x in Keywords)))
        char_stream = CharStream(stream)
        lexer = lexer = Lexer(char_stream, self.__class__.tokenizer)
        result = [x.ttype for x in lexer if not repr(x.ttype).endswith('WS')]
        self.assertEqual([repr(x) for x in Keywords], [repr(x) for x in result])

class ParserTest(unittest.TestCase):
    pass
