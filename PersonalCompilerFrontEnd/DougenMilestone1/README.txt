These files contain the code for a simple starter compiler used in CS 161. To start with, the simple programming language syntax contains variable declarations, assignment statements, input and output statements. Mathematical expressions with multiplication and addition of integers are supported. 

All code is written for Python 3.

The files are as follows:

AST.py - A file with class definitions for an abstract syntax tree representation of the program being compiled
README.txt - this file
sampleProgram.prg - an example program written in a simple programming language syntax
LastLighthous_lexer.py - The PLY Lex definitions of the language's tokens
starter_parser.py - The PLY Yacc implementation of language syntax. This parser builds an AST which is then used to generate three address code.


To run this compiler, run the following at a command prompt:

python starter_parser.py


By default, this will wait for you type in the program at standard input. If you would like to compile a program from a file, like sampleProgram.prg, you can run a command like cat (on Mac/Unix/Linux) or type (on Windows) to display the file contents and then pipe them into the compiler with a command like

cat sampleProgram.prg | python starter_parser.py

or

type sampleProgram.prg | python starter_parser.py

To save the results to a file such as result.tac, redirect the output with a command like 

cat sampleProgram.prg | python starter_parser.py > result.tac

or

type sampleProgram.prg | python starter_parser.py > result.tac


9/16/2019 Update

A quick change of NUM (r'\d+') allowed multi-digit integer literals to be accepted.

A NEWLINE token was added to count the occurence of \n. \n was removed from t_ignore.

A COMMENT token was added so the lexer, when it encounters ~!, treats any following text as a comment. This continues until it recognizes \n.

A MLCOMMENT (multi-line comment) token was added so the lexer, when it encounters ~!~, treats any following text as a comment. This continues until a second ~!~ is recognized.

t_error was updated soit will print the line number an illegal character occurred on using t.lexer.lineno.

Three data variables were added to test the lexer. They are put into the lexer seperately through lexer.input(data) and the tokens are displayed in For loops.
These serve as the test cases for the program and can be demnstrated simply by running the file.

Self-Assessment:
The first part of the assignment was easy enough. r'\d' just had to be changed to r'\d+' to allow one or more digits. The second part was harder, but only because it took me forever to realize
t_ignore was overriding the NEWLINE function. I don't know how how it did this even when I had commented the line of code out, but it did. Once I removed \n from t_ignore, NEWLINE worked. Figuring
out which line an illegal character occurred on was as simple as adding t.lexer.lineno to t_error's print statement. Finally, I had to add comments and multi-line comments. For the comment, I created
a regular expression that must start with ~!, can include any word, number, and a few symbols that are likely to be used in comments and must end with a newline (to make sure it's a single line comment).
The multi-line comment was the same with three main differences: it must start with ~!~, it can contain newlines, and it must end with ~!~.   

Because I couldn't get the manual input code to work, I don't think it can work in Anaconda's Spyder workspace, I opted to test the code with strings contained in the file. data1, data2, and data3 test 
multi-digit integer recognition, erorr handling and line counting, and comment and multi-comment features of the code, repesctively. In the future, I want to add some ability for the code to read files,
but I believe this should work for know until I figure that out. Overall, there are definitely ways to improve the code I added. The COMMENT and MLCOMMENT tokens could have more symbols added to them. For now,
the code accomplishes the goals of the assignment.