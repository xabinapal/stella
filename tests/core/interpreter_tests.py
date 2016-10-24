# -*- coding: utf-8 -*-

from stella.core.utils import CharStream
from stella.core.interpreter.lexer import Tokenizer, Lexer
from stella.core.interpreter.parser import Parser
from stella.core.grammar import Keywords, Tokens

import io
import unittest

_simple_script = '''
    while (i--) {
        if (i % 3 == 1) {
            j++;
        }
    }
'''

class LexerTest(unittest.TestCase):
    tokenizer = Tokenizer(Tokens)

    def test_notoken(self):
        stream = io.StringIO('ñ')
        char_stream = CharStream(stream)
        lexer = Lexer(char_stream, self.__class__.tokenizer)
        self.assertIsNone(next(lexer).ttype)

    def test_keywords(self):
        stream = io.StringIO(';'.join((x.expr for x in Keywords)))
        char_stream = CharStream(stream)
        lexer = Lexer(char_stream, self.__class__.tokenizer)
        result = (x.ttype for x in lexer if not x.ttype.name == 'SEMICOLON')
        self.assertEqual([repr(x) for x in Keywords], [repr(x) for x in result])

    def test_simple_script(self):
        lexer = Lexer(_simple_script, self.__class__.tokenizer)

        result = [x.value for x in lexer if not x.ttype.name == 'WSPACE'
            and not x.ttype.name == 'NLINE']
        self.assertEqual(''.join(result), 'while(i--){if(i%3==1){j++;}}')

class ParserTest(unittest.TestCase):
    pass
