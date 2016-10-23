# -*- coding: utf-8 -*-

from stella.core.utils import Rewinder
from stella.core.interpreter.lexer import Tokenizer, Lexer, LexError
from stella.core.interpreter.productions import StatementType
from stella.core.automata import ENFA, Epsilon

__all__ = ['ParseError', 'Parser']

################################################################################
### ParseError
################################################################################

class ParseError(SyntaxError):
    pass
    
################################################################################
### Parser
################################################################################

class Parser(object):
    def __init__(self, lexer, statement, automata, ignore=[]):
        self.lexer = Rewinder(lexer)
        self.statement = statement
        self.automata = automata
        self.ignore = ignore
        self.ignore_until = None

    def __iter__(self):
        return Rewinder(self)

    def __next__(self):
        self.lexer.peek() # if no tokens left, raises an StopIteration
        automaton = self.automata[self.statement]
        automaton.reset()
        
        while automaton.valid_state() and not automaton.accepting_state():
            token = self._get_token()
            automaton.input(token)

            for t in automaton.current_transitions():
                if t != Epsilon:
                    state = StatementType.parse_str_repr(t[1:-1])
                    if state:
                        Parser(self.lexer, state, self.automata, self.ignore)

        if not automaton.valid_state():
            raise ParseError()

        return automaton

    def _get_token(self):
        ignore_token = True
        while ignore_token:
            try:
                token = next(self.lexer)
                ignore_token = self._ignored_token(token)
            except StopIteration as e:
                if self.ignore_until:
                    raise ParseError()

                raise e

        return token

    def _ignored_token(self, token):
        if self.ignore_until:
            if token.ttype == self.ignore_until:
                self.ignore_until = None
            return True

        if not token.ttype:
            raise ParseError('Unexpected token ' + token.value)

        ignore = (x for x in self.ignore if x[0] == token.ttype)
        ignore = next(ignore, None)

        if ignore:
            self.ignore_until = ignore[1] if len(ignore) > 1 else None
            return True

        return False
