'''
File: LastLighthouse_back_lexer.py

This is Python Lex code defining tokens for the intermediate three address code
used in the Drake University Compiler Construction course (CS 161)

Author: Noah Dougen

Last Updated: 11/25/2019

'''
import ply.lex as lex

#a dictionary mapping reserved word lexemes to token names
reserved = {
	'read' : 'READ',
	'write' : 'WRITE',
        'IfFalse' : 'IFFALSE',
        'Else' : 'ELSE',
        'goto' : 'GOTO',
        'length' : 'LENGTH',
}

#this is the list of all tokens in our language
#it includes the reserved words
tokens = [
	'COLON',
        'COMMA',
        'LSQUARE',
        'RSQUARE',
        'UNARYNOT',
	'TIMES',
        'DIVIDE',
	'PLUS',
        'MINUS',
        'LESSTHAN',
        'GREATERTHAN',
        'LESSEQUAL',
        'GREATEQUAL',
        'EQUALTO',
        'NOTEQUAL',
        'AND',
        'OR',
	'ASSIGN',
	'NUM',
	'ID'
	]+list(reserved.values())


# Regular expression rules for simple tokens
t_COLON = r':'
t_COMMA = r','
t_LSQUARE = r'\['
t_RSQUARE = r'\]'
t_UNARYNOT = r'\!'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_PLUS = r'\+'
t_MINUS = r'\-'
t_LESSTHAN = r'<'
t_GREATERTHAN = r'>'
t_LESSEQUAL = r'<='
t_GREATEQUAL = r'>='
t_EQUALTO = r'=='
t_NOTEQUAL = r'\!='
t_AND = r'&&'
t_OR = r'\|\|'
t_ASSIGN = r'='

#matching identifiers - starting with a letter or underscore
#followed by any number of letters, numbers, and underscores
def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'

	#reserved words get their own
	#token type, not ID
	if t.value in reserved:
		t.type = reserved[t.value]

	return t

#this regular expression will match a single digit
def t_NUM(t):
	r'\d+'
	t.value = int(t.value)    
	return t

# A string containing ignored characters (spaces, tabs, and newlines)
t_ignore  = ' \t\n'

def t_error(t):
	print('Illegal character:',t.value[0])
	t.lexer.skip(1)


lexer = lex.lex()
