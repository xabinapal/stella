# -*- coding: utf-8 -*-

import itertools

from stella.core.utils import Rewinder
from stella.core.interpreter import Tokenizer, Lexer, LexError
from stella.core.interpreter.tokens import _TokenType

__all__ = ['ParseError', 'Parser']

################################################################################
### ParseError
################################################################################

class ParseError(SyntaxError):
    pass

################################################################################
### _ParserStatementLexer
################################################################################

_ParserToken = _TokenType()

class _ParserStatementLexer(object):
    parserTokens = (
        _ParserToken.LBRACE(r'\{'),
        _ParserToken.RBRACE(r'\}'),
        _ParserToken.LPAREN(r'\('),
        _ParserToken.RPAREN(r'\)'),
        _ParserToken.VBAR(r'\|'),
        _ParserToken.PLUS(r'\+'),
        _ParserToken.QUESTION(r'\?'),
        _ParserToken.GROUP(r'(t|s)(\.([a-zA-Z\.]+)?)?')
    )

    def __init__(self, statements):
        self.tokenizer = Tokenizer(self.__class__.parserTokens)
        self.statements = statements

    def get_automata(self):
        return (self.get_automaton(x) for x in self.statements)

    def get_automaton(self, statement):
        lexer = iter(Lexer(statement.expr, self.tokenizer))
        groups = [x for x in self._get_groups(lexer)]
        return self._create_automaton(groups)

    def _get_groups(self, lexer):
        pass

    def _create_automaton(self, groups):
        nodes = len(groups) + 1
        transitions = [[-1 for i in range(nodes)] for i in range(nodes)]

################################################################################
### Parser
################################################################################

class Parser(object):
    def __init__(self, lexer, statements, ignore=[]):
        self.dfa = _ParserStatementLexer(statements).get_automata()
        self.lexer = Rewinder(lexer)
        self.ignore = zip(ignore)
        self.ignore_until = None

    def __iter__(self):
        return Rewinder(self)

    def __next__(self):
        valid_token = False
        while not valid_token:
            try:
                token = next(self.lexer)
            except StopIteration:
                if self.ignore_until:
                    raise ParseError()

            valid_token = self._is_valid_token(token)

        return token

    def _is_valid_token(self, token):
        if self.ignore_until:
            if token == self.ignore_until:
                self.ignore_until = None
            return False

        if not token.ttype:
            raise ParseError(token.value)

        ignore = (x for x in self.ignore if x[0] == token.ttype)
        ignore = next(ignore_token, None)

        if ignore:
            self.ignore_until = ignore[1] if len(ignore) > 1 else None
            return False

        return True
