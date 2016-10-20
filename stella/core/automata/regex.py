from stella.core.interpreter import _TokenType, Tokenizer, Lexer
from stella.core.automata import NFA
from stella.core.utils import CharStream

__all__ = ['RegexToken', 'regex_to_nfa']

RegexToken = _TokenType()

_lparen = RegexToken.LPAREN(r'\(')
_rparen = RegexToken.RPAREN(r'\)')
_question = RegexToken.QUESTION(r'\?')
_plus = RegexToken.PLUS(r'\+')
_asterisk = RegexToken.ASTERISK(r'\*')
_verticalbar = RegexToken.VERTICALBAR(r'\|')

_tokens = (_lparen, _rparen, _question, _plus, _asterisk)

def regex_to_nfa(regex, token, equal):
    stream = CharStream(regex)
    tokens = (*_tokens, token)
    tokenizer = Tokenizer(tokens)
    lexer = Lexer(stream, tokenizer)
    return _lexer_to_nfa(lexer, equal)

def _lexer_to_nfa(lexer, equal, end=None):
    nfa = NFA()

    for x in stream:
        if end and equal(end, x):
            lexer.commit()
            return nfa

        if x.ttype == _lparen:
            lexer.commit()
            nfa.add_sub_nfa(_lexer_to_nfa(lexer, equal, _rparen))
        elif x.ttype not in _tokens:
            nfa.add_operand(x.value)
        else:
            nfa.modify_last_operand(x.value)

    return nfa
