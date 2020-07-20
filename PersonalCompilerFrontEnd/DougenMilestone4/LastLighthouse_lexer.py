'''
File: LastLighthouse_lexer.py

This is Python Lex code defining tokens for a small C-like language
used in the Drake University Compiler Construction course (CS 161)

Author: Noah Dougen

Last Updated: 9/15/2019

'''
import ply.lex as lex
import sys

#a dictionary mapping reserved word lexemes to token names
reserved = {
	'read' : 'READ',
	'write' : 'WRITE',
	'int' : 'INT',
        'if' : 'IF',
        'else' : 'ELSE',
        'while' : 'WHILE'
}

#this is the list of all tokens in our language
#it includes the reserved words
tokens = [
	'LPAREN',
	'RPAREN',
	'LBRACE',
	'RBRACE',
	'SEMICOLON',
        'UNARYNOT',
	'TIMES',
        'DIVIDE',
        'MODULUS',
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
	'ID',
        'NEWLINE',
        'COMMENT',
        'MLCOMMENT'
	]+list(reserved.values())


# Regular expression rules for simple tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_UNARYNOT = r'\!'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULUS = r'%'
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

#Define a rule so we can track line numbers
def t_NEWLINE(t):                                          
     r'\n+'                                             
     t.lexer.lineno += len(t.value) 
     
#Define a rule so the programmer can write comments     
def t_COMMENT(t):                                          
     r"(~!)(\d|\s|\w|\.|\?|!|,|'|;)*(~!)"
     return t
 
#Define a rule so the programmer can write multi-line comments
def t_MLCOMMENT(t):                                        
     r"(~!~)(\d|\s|\w|\n|\.|\?|\!|,|'|;)*(~!~)"
     return t
    
# A string containing ignored characters (spaces, tabs, and newlines)
t_ignore  = ' \t'

def t_error(t):
	print('Illegal character:',t.value[0], 'Found on line:', t.lexer.lineno)     
	t.lexer.skip(1)


lexer = lex.lex()
                                  
                            
