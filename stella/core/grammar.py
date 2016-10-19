# -*- coding: utf-8 -*-

from stella.core.interpreter.tokens import TokenType
from stella.core.interpreter.statements import StatementType

__all__ = ['Tokens, Statements']

################################################################################
### Keywords
################################################################################

Keyword = TokenType.Keyword()
FlowControl = Keyword.FlowControl()
DataType = Keyword.DataType()

FlowControlKeywords = (
    Keyword.FlowControl.FUNCTION(r'function'),
    Keyword.FlowControl.IF(r'if'),
    Keyword.FlowControl.ELSE(r'else'),
    Keyword.FlowControl.WHILE(r'while'),
    Keyword.FlowControl.FOR(r'for'),
    Keyword.FlowControl.BREAK(r'break'),
    Keyword.FlowControl.CONTINUE(r'continue'),
    Keyword.FlowControl.RETURN(r'return'),
)

DataTypeKeywords = (
    Keyword.DataType.INTEGER('int'),
    Keyword.DataType.FLOATING('float'),
)

Keywords = FlowControlKeywords + DataTypeKeywords

################################################################################
### Identifiers
################################################################################

Identifier = TokenType.Identifier()
Comment = Identifier.Comment()

Identifiers = (
    Identifier.LITERAL(r'[a-zA-Z_][a-zA-Z0-9_]*'),
    Identifier.WS(r'[\s\t]+'),
    Identifier.NEWLINE(r'\r?\n'),
    Comment.STR(r'/\*'),
    Comment.END(r'\*/'),
    Comment.LINE(r'//.*\n?'),
)

################################################################################
### Constants
################################################################################

Constant = TokenType.Constant()
IntegerConstant = Constant.IntegerConstant()
FloatingConstant = Constant.FloatingConstant()

Constants = (
    IntegerConstant.DECIMAL(r'(0|[1-9][0-9]*)'),
    IntegerConstant.HEXADECIMAL(r'0x[a-fA-F0-9]*'),
    IntegerConstant.OCTAL(r'0[0-7]+'),
    IntegerConstant.BINARY(r'0b[0-1]*'),
    FloatingConstant.DECIMAL(r'([0-9]+\.[0-9]*|[0-9]*\.[0-9]+)'),
)

################################################################################
### Punctuators
################################################################################

Punctuator = TokenType.Punctuator()

Punctuators = (
    Punctuator.LBRACK(r'\['),
    Punctuator.RBRACK(r'\]'),
    Punctuator.LPAREN(r'\('),
    Punctuator.RPAREN(r'\)'),
    Punctuator.LBRACE(r'\{'),
    Punctuator.RBRACE(r'\}'),

    Punctuator.DOT(r'\.'),
    Punctuator.COMMA(r','),
    Punctuator.SEMICOLON(r';'),
    Punctuator.EQUAL(r'='),

    Punctuator.INC(r'\+'),
    Punctuator.DEC(r'-'),
    Punctuator.MUL(r'\*'),
    Punctuator.DIV(r'/'),
    Punctuator.MOD(r'%'),

    Punctuator.LSHIFT(r'<<'),
    Punctuator.RSHIFT(r'>>'),
    Punctuator.LROT(r'<<<'),
    Punctuator.RROT(r'>>>'),

    Punctuator.AND(r'&'),
    Punctuator.OR(r'\|'),
    Punctuator.XOR(r'\^'),
    Punctuator.NOT(r'~'),

    Punctuator.INC_OP(r'\+\+'),
    Punctuator.DEC_OP(r'--'),
    Punctuator.AND_OP(r'&&'),
    Punctuator.OR_OP(r'\|\|'),
    Punctuator.NOT_OP(r'!'),

    Punctuator.LT_OP(r'<'),
    Punctuator.GT_OP(r'>'),
    Punctuator.LEQ_OP(r'<='),
    Punctuator.GEQ_OP(r'>='),
    Punctuator.EQ_OP(r'=='),
    Punctuator.NEQ_OP(r'!='),
)

################################################################################
### Tokens
################################################################################

Tokens = Keywords + Identifiers + Constants + Punctuators

################################################################################
### Statements
################################################################################

Jump = StatementType.Jump()

JumpStatements = (
    Jump.Break(r'{t.BREAK}{t.SEMICOLON}'),
    Jump.Continue(r'{t.CONTINUE}{t.SEMICOLON}'),
)

Control = StatementType.Control()

ControlStatements = (
    Control.If(r''),
    Control.IfElse(r''),
    Control.While(r''),
    Control.For(r'')
)

Statements = (
    StatementType.Empty(r'{t.SEMICOLON}'),
    StatementType.Block(r'{t.LBRACE}{s}{t.RBRACE}'),

    StatementType.FunctionArguments(
        r'{t.DataType}{t.LITERAL}({t.COMMA}{s.FunctionArguments})?'),

    StatementType.FunctionArgumentList(
        r'{t.LPAREN}{s.FunctionArguments}?{t.RPAREN}'),
    
    StatementType.Function(
        r'{t.FUNCTION}{t.DataType}{t.LITERAL}{t.FunctionArgumentList}{s.Block}'),
)

Statements = JumpStatements + ControlStatements
