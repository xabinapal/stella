# -*- coding: utf-8 -*-

from stella.core.interpreter.productions import TokenType, StatementType

__all__ = ['Tokens', 'Statements', 'ProgramStatement']

################################################################################
### Keywords
################################################################################

Keyword = TokenType.Keyword()
FlowControl = Keyword.FlowControl()
DataType = Keyword.DataType()

FlowControlKeywords = (
    FlowControl.FUNCTION(r'function'),
    FlowControl.IF(r'if'),
    FlowControl.ELSE(r'else'),
    FlowControl.WHILE(r'while'),
    FlowControl.FOR(r'for'),
    FlowControl.BREAK(r'break'),
    FlowControl.CONTINUE(r'continue'),
    FlowControl.RETURN(r'return'),
)

DataTypeKeywords = (
    DataType.INTEGER('int'),
    DataType.FLOATING('float'),
)

Keywords = FlowControlKeywords + DataTypeKeywords

################################################################################
### Identifiers
################################################################################

Identifier = TokenType.Identifier()
Comment = Identifier.Comment()

_literal = Identifier.LITERAL(r'[a-zA-Z_][a-zA-Z0-9_]*')
_whitespace = Identifier.WSPACE(r'[\s\t]+')
_newline = Identifier.NLINE(r'\r?\n')
_comment_line = Comment.LINE(r'//.*\n?')
_comment_start = Comment.START(r'/\*')
_comment_end = Comment.END(r'\*/')

Identifiers = (
    _literal, _whitespace, _newline,
    _comment_line, _comment_start, _comment_end,
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
IgnoreTokens = (
    (_whitespace,),
    (_newline,),
    (_comment_line,),
    (_comment_start, _comment_end),
)

################################################################################
### Statements
################################################################################

ProgramStatement = StatementType.Program(r'{s.FunctionDeclaration}*')

Function = StatementType.Function()

FunctionStatements = (
    Function.FunctionFirstArgument(r'{t.DataType}{t.LITERAL}'),
    Function.FunctionNextArgument(r'{t.COMMA}{s.FunctionFirstArgument}'),
    Function.FunctionArguments(r'{s.FunctionFirstArgument}{s.FunctionNextArgument}+?'),
    Function.FunctionArgumentList(r'{t.LPAREN}{s.FunctionArguments}?{t.RPAREN}'),
    Function.FunctionDeclaration(r'{t.FUNCTION}{t.DataType}{t.LITERAL}{s.FunctionArguments}{s.Block}'),
)

Jump = StatementType.Jump()

JumpStatements = (
    Jump.Break(r'{t.BREAK}{t.SEMICOLON}'),
    Jump.Continue(r'{t.CONTINUE}{t.SEMICOLON}'),
)

Block = StatementType.Block()

BlockStatements = (
    Block.RegularBlock(r'{t.LBRACE}({s.Statement}|{s.RegularBlock}){t.RBRACE}'),
    Block.LoopBlock(r'{t.LBRACE}({s.Jump}|{s.Statement}|{s.RegularBlock}){t.RBRACE}'),
)

Control = StatementType.Control()

ControlStatements = (
    Control.If(r'{t.IF}{t.LPAREN}{t.RPAREN}{s.RegularBlock}'),
    Control.IfElse(r'{s.If}{t.ELSE}{s.RegularBlock}'),
    Control.While(r'{t.WHILE}{t.LPAREN}{t.RPAREN}{s.RegularBlock}'),
    Control.For(r'{t.FOR}{t.LPAREN}{t.RPAREN}{s.RegularBlock}'),
)

Statements = (
    StatementType.Empty(r'{t.SEMICOLON}'),
)

Statements = (ProgramStatement,) + FunctionStatements + JumpStatements #JumpStatements + ControlStatements
