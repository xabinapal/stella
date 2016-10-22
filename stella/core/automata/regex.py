# -*- coding: utf-8 -*-

from stella.core.interpreter.tokens import _TokenType
from stella.core.interpreter.lexer import Tokenizer, Lexer
from stella.core.automata import ENFA, EpsilonTransition
from stella.core.utils import CharStream

import io

__all__ = ['RegexToken', 'convert_to_enfa']

RegexToken = _TokenType()

_lparen = RegexToken.LPAREN(r'\(')
_rparen = RegexToken.RPAREN(r'\)')
_union  = RegexToken.UNION(r'\|')
_star   = RegexToken.STAR(r'\*')

_tokens = (_lparen, _rparen, _union, _star)

def _create_lexer(regex, token):
    regex = io.StringIO('(' + regex + ')')
    stream = CharStream(regex)
    tokenizer = Tokenizer((*_tokens, token))
    lexer = Lexer(stream, tokenizer)
    return lexer

def _symbol_checker(symbol_table, symbol):
    if EpsilonTransition == symbol:
        return symbol_table[symbol] if symbol in symbol_table else []

    table_match = next((x for x in symbol_table if symbol.ttype.is_of(x)), None)
    return symbol_table[table_match]

def convert_to_enfa(regex, token):
    token = RegexToken.TOKEN(token)
    lexer = _create_lexer(regex, token)
    enfa = ENFA(symbol_checker=_symbol_checker)
    enfa.add_state(0, initial=True, accepting=False)
    enfa.add_transition(0, 1, EpsilonTransition)

    lparen_pos = None
    unions = []

    for x in lexer:
        i = enfa.state_count
        enfa.add_state(i)

        if x.ttype == token:
            enfa.add_transition(i, i + 1, x.value)
        elif x.ttype == _union:
            enfa.add_transition(lparen_pos, i, EpsilonTransition)
        else:
            enfa.add_transition(i, i + 1, EpsilonTransition)

            if x.ttype in _lparen:
                lparen_pos = i
            
            elif x.ttype in _rparen:
                while unions:
                    enfa.add_transition(unions.pop(), i, EpsilonTransition)
                lparen_pos = None

            elif x.ttype == _star:
                enfa.add_transition(i, i - 1, EpsilonTransition)
                enfa.add_transition(i - 1, i, EpsilonTransition)

    enfa.add_state(name=enfa.state_count, accepting=True)

    return enfa
