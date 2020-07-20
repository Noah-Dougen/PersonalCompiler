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

t_error was updated so it will print the line number an illegal character occurred on using t.lexer.lineno.

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

10/9/19 Update

The parser and lexer where updated so one can manually input code through a console.

A symbol table was added to the starter_parser, newly dubbed LastLighthouse_parser, that tracks
which IDs have been declared and where they are being used.

A for-loop is present anywhere the ID symbol is called that checks to see if a the ID has been
declared and is preset in the symbol_table_list. 

An error is reported if an ID is used without appearing in the symbol table (undeclared). This
occurs both when the user attempts to assign an ID a value and when a variable is used in an
expression.

In a nested scope, variables are distinguished by scope_level. When a scope level is declared,
scope_level increases by one, meaning ID x would be declared as x1 in the first level and x2
in the second level. When a nested scope is exited, the scope_level decreases by 1. This means
x can be declared in both an outer scope and an inner scope.

Noteable bugs:
If a user enters a nested scope, exits to the outer scope, and enters into a new nested scope,
that scope will share the same scope level with the previous nested scope. This will be fixed
in the future with a list that keeps track of what scope levels have been used.

Self-Assessment:
To allow the parser to recognize and note declared IDs, I first added a symbol table at the top.
A ID was added to the symbol table when it was declared, and the symbol table was added to a
larger symbol table list. Then a for-loop goes through each symbol table to find a declared ID.
This part, once I could find everywhere the for-loop should be present, was easy enough.

To deal with nested scopes, I created a scope level counter that keeps track of what scope an
ID is in. When an ID is declared it is concatenated with the scope level (x in scope 1 becomes
x1). This part presented some issues, mainly figuring out how to have the for-loop recognize
the altered ID. I did this by attaching the scope level anywhere the program checked ID,
including the for-loops. The scope level still has some issues. Namely, the issue noted in the
noteable bugs section. This will either be fixed by adding code that recognizes when a newly
declared scope has already been used, or by disallowing a user the user to create multiple
nested scopes at the same level within an outer scope.  

I only needed four test files for the program. The tests below include output that explian what
is happening. 
Test 1 shows a declared variable would be recognized both when used in an expression and an
assignment:
{
	int x; 
	x = 3;
	x = x + 2;
}
Output:
{
	declaring x1 as None on line 2
	symbol x1 : ('x1', 'line 2')    # x = 3;
	symbol x1 : ('x1', 'line 2')    # x = ...
	symbol x1 : ('x1', 'line 2')    # = x + 2;
}

Test 2 shows that an error is printed when a variable is assigned before it is declared. It also
shows that x can be properly read and written:
{ 
	x = 5; 
	int x;
	x = 3;
	read x;
	write x;
}
Output:
{
Error: x1 is not in the symbol table   # x = 5; x used before declaration
	declaring x1 as None on line 3
	symbol x1 : ('x1', 'line 2')    # x = 3;
	symbol x1 : ('x1', 'line 2')    # read x;
	symbol x1 : ('x1', 'line 2')    # write x;
}

Test 3 shows that an error is printed if a variable is used in an expression before it is 
declared:
{
	int x;
	x = 9 + y;
}
Output:
{
	declaring x1 as None on line 2   
Error: y1 is not in the symbol table    # x = 9 + y; y is used before declaration
	symbol x1 : ('x1', 'line 2')    # x = ...

Test 4 shows that a nested scope will can share the same variable name with the outer scope:
{ 
	int x;
	int z;
	x = 7;
	
	{
		int x;
		x = 5;
	}
	z = 2;
}
Output:
{
	declaring x1 as None on line 2
	declaring z1 as None on line 3
	symbol x1 : ('x1', 'line 2')   # x = 7; declared in scope 1
	{
		declaring x2 as None on line 7
		symbol x2 : ('x2', 'line 7')   # x = 5; declared in scope 2
	}
	symbol z1 : ('z1', 'line 3')   # x = 2; declared in scope 1
}

10/28/19 Update:

The lexer, parser, and AST were all updated to add additional operators. The AST, renamed 
LastLighthouse_AST, connects to the parser so input into the parser generates three-address
code.

Three branches were added to the grammar: lowop, equal, and op. In order of lowest precedence
to highest: AND and OR statements were added to the lowop branch. EQUAL TO and NOT EQUAL TO 
operators were added to equal. GREATER THAN, LESS THAN, GREATER OR EQUAL TO, and LESS THAN OR
EQUAL TO were added to op. MINUS was added to expr. DIVIDE and MODULUS were added to term. 
Finally, UNARY MINUS and UNARY NOT were added to factor. Tokens for all of these operators were
also added to the lexer. In the AST, a UnaryNode was added that take in two values: the unary
operator and the value attached to it.

Self-Assessment:
To complete the first part, I simply added every new operator to the lexer's tokens with the
exception of UNARY NOT. Becuase it would conflict with MINUS, I just reused MINUS. This was by
far the easiest part of the assignment. All the test files demonstrate the lexer in action.

Next I had to update the lexer to accept the new operators. This was abit trickier. To get the right
precedence, I created three new branches to the grammar, lowop, equal, and op; and added them
between stmt and expr. Anywhere expr appeared outside of the expr branch was replaced with lowop.
For the unary operators, I added "factor: MINUS factor" and "factor: UNARYNOT factor" to the
factor branch. This established the correct precedence, which meant I only had to line-up the
AST inputs (p[1], p[2], etc.) and uncomment the gen() function. This was the most time 
consuming part of the assignment. All the test files demonstrate proper precedence.

Finally, I had to change the AST. Aside from the unary operators, every new operator could be 
handled with the already existing BinaryNode. I created a new UnaryNode that took in two arguments.
After a lot of tinkering and getting some help, I was able to make the node print out three-
address code with a unary value and an attached value. This is demonstrated in Test4. 
Unfortunately, I was unable to figure out how to incorporate short-circuit logical operators.

Overall, the new code appears to be able to print proper three-address code while reading in
values using the correct precedence. It also sports many new operators.
