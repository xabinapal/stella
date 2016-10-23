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

    def get_ast(self):
        automaton = self.automata[self.statement]
        automaton.reset()

        inputs = []
        print(self.statement)
        while automaton.valid_state() and not automaton.accepting_state():
            is_statement = False

            for t in automaton.current_transitions():
                state = StatementType.parse_str_repr(t)
                if state:
                    self.lexer.commit()
                    p = Parser(self.lexer, state, self.automata, self.ignore)
                    try:
                        sub_ast = p.get_ast()
                        inputs.append(sub_ast)
                        automaton.input(t)
                        is_statement = True
                        self.lexer.commit()
                        break
                    except ParseError:
                        self.lexer.rewind()
                        pass

            if not is_statement:
                self.lexer.commit()
                token = self._get_token()
                print(token)
                inputs.append(token)
                automaton.input(token)

        if not automaton.valid_state():
            raise ParseError()

        return inputs

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
