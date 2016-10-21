from stella.core.interpreter.tokens import _TokenType
from stella.core.interpreter.lexer import Tokenizer, Lexer
from stella.core.automata import NFA, EpsilonTransition
from stella.core.utils import CharStream

import io

__all__ = ['RegexToken', 'convert_to_nfa']

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

def convert_to_nfa(regex, token):
    token = RegexToken.TOKEN(token)
    lexer = _create_lexer(regex, token)
    nfa = NFA()

    lparen_pos = None
    unions = []

    for x in lexer:
        i = nfa.state_count
        nfa.add_state(i)

        if x.ttype == token:
            nfa.add_transition(i, i + 1, x.value)
        elif x.ttype == _union:
            nfa.add_transition(lparen_pos, i, EpsilonTransition)
        else:
            nfa.add_transition(i, i + 1, EpsilonTransition)

            if x.ttype in _lparen:
                lparen_pos = i
            
            elif x.ttype in _rparen:
                while unions:
                    nfa.add_transition(unions.pop(), i, EpsilonTransition)
                lparen_pos = None

            elif x.ttype == _star:
                nfa.add_transition(i, i - 1, EpsilonTransition)
                nfa.add_transition(i - 1, i, EpsilonTransition)

    nfa.add_state(name=nfa.state_count, accepting=True)

    return nfa
