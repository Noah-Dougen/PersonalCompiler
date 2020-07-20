'''
File: starter_lexer.py

This is Python Lex code defining tokens for a small C-like language
used in the Drake University Compiler Construction course (CS 161)

Author: Eric D. Manley

Last Updated: 8/21/2019

'''
import ply.lex as lex

#a dictionary mapping reserved word lexemes to token names
reserved = {
	'read' : 'READ',
	'write' : 'WRITE',
	'int' : 'INT'
}

#this is the list of all tokens in our language
#it includes the reserved words
tokens = [
	'LPAREN',
	'RPAREN',
	'LBRACE',
	'RBRACE',
	'SEMICOLON',
	'TIMES',
	'PLUS',
	'ASSIGN',
	'NUM',
	'ID'
	]+list(reserved.values())


# Regular expression rules for simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_TIMES = r'\*'
t_PLUS = r'\+'
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
	r'\d'
	t.value = int(t.value)    
	return t

# A string containing ignored characters (spaces, tabs, and newlines)
t_ignore  = ' \t\n'

def t_error(t):
	print('Illegal character:',t.value[0])
	t.lexer.skip(1)


lexer = lex.lex()
