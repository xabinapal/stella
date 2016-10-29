# -*- coding: utf-8 -*-

from stella.core.utils import RewindableIterator
from stella.core.interpreter.lexer import Tokenizer, Lexer
from stella.core.interpreter.productions import StatementType
from stella.core.automata import ENFA, Epsilon

import abc

__all__ = ['ParseError', 'Parser', 'RDParser', 'TDOPParser']

################################################################################
### ParseError
################################################################################

class ParseError(SyntaxError):
    pass
    
################################################################################
### Parser
################################################################################

class Parser(metaclass=abc.ABCMeta):
    pass

################################################################################
### RDParser
################################################################################

class RDParser(Parser):
    def __init__(self, lexer, statement, automata, ignore=[]):
        if isinstance(lexer, RewindableIterator):
            self.lexer = lexer.clone()
        else:
            self.lexer = RewindableIterator(lexer)

        self.statement = statement
        self.automata = automata
        self.ignore = ignore
        self.ignore_until = None

    def get_ast(self):
        automaton = self.automata[self.statement]
        automaton.reset()

        inputs = []
        last_was_accepting = False
        print(self.statement)
        while automaton.valid_state:
            if not [x for x in automaton.current_transitions if x != Epsilon]:
                break

            last_was_accepting = automaton.accepting_state
            next_input = self._get_next_input(automaton)
            if automaton.valid_state:
                inputs.append(next_input)
                self.lexer.commit()

        self.lexer.rewind()
        if not automaton.valid_state and not last_was_accepting:
            raise ParseError()

        return self._create_ast(inputs)

    def _get_next_input(self, automaton):
        self.lexer.commit()
        next_input = None
        is_statement = False

        for t in automaton.current_transitions:
            state = StatementType.parse_str_repr(t)
            if state:
                parser = state.parser if state.parser else self._class__
                p = parser(self.lexer, state, self.automata, self.ignore)
                try:
                    next_input = p.get_ast()
                    automaton.input(t)
                    is_statement = True
                    self.lexer.delete()
                    self.lexer = p.lexer
                    break;
                except ParseError:
                    p.lexer.delete()
                    pass

        if not is_statement:
            next_input = self._get_token()
            automaton.input(next_input)
            if automaton.valid_state:
                print(next_input)

        return next_input

    def _get_token(self):
        ignore_token = True
        while ignore_token:
            try:
                token = next(self.lexer)
                ignore_token = self._ignored_token(token)
            except StopIteration as e:
                if self.ignore_until:
                    raise ParseError('Expecting ' + str(self.ignore_until.ttype) + ', found <EOF>')

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

    def _create_ast(self, inputs):
        return inputs
    
################################################################################
### TDOPParser
################################################################################

class TDOPParser(Parser):
    pass
