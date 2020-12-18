%{ 	 
    #include <stdio.h>
    int lineNumber = 1;
    int correct = 1;
    int badLine = 0;
%} 
%option noyywrap

digit 		        [0-9]
nonZeroDigit        [1-9]
letter              [a-zA-Z]
character_constant  [']([a-zA-Z_?! ])*[']
numerical_constant  [-]?{nonZeroDigit}{digit}*|0
constant            {character_constant}|{numerical_constant}
identifier          {letter}|{letter}({letter}|{digit}|_)*?


%% 

"main" {printf( "%s - reserved word\n", yytext );}
"define" {printf( "%s - reserved word\n", yytext );}
"Integer" {printf( "%s - reserved word\n", yytext );}
"Char" {printf( "%s - reserved word\n", yytext );}
"while" {printf( "%s - reserved word\n", yytext );}
"for" {printf( "%s - reserved word\n", yytext );}
"if" {printf( "%s - reserved word\n", yytext );}
"else" {printf( "%s - reserved word\n", yytext );}
"in.Integer" {printf( "%s - reserved word\n", yytext );}
"in.Chars" {printf( "%s - reserved word\n", yytext );}
"out" {printf( "%s - reserved word\n", yytext );}

{identifier} {printf( "Identifier: %s\n", yytext );}
{constant}	{printf( "Constant: %s\n", yytext );}

"[" {printf("%s - as separator\n", yytext);}
"]" {printf("%s - as separator\n", yytext);}
"{" {printf("%s - as separator\n", yytext);}
"}" {printf("%s - as separator\n", yytext);}
"(" {printf("%s - as separator\n", yytext);}
")" {printf("%s - as separator\n", yytext);}
";" {printf("%s - as separator\n", yytext);}
"," {printf("%s - as separator\n", yytext);}

"+" {printf("%s - as operator\n", yytext);}
"-" {printf("%s - as operator\n", yytext);}
"*" {printf("%s - as operator\n", yytext);}
"/" {printf("%s - as operator\n", yytext);}
"%" {printf("%s - as operator\n", yytext);}
">>" {printf("%s - as operator\n", yytext);}
"<=" {printf("%s - as operator\n", yytext);}
">=" {printf("%s - as operator\n", yytext);}
"==" {printf("%s - as operator\n", yytext);}
"!=" {printf("%s - as operator\n", yytext);}
"=" {printf("%s - as operator\n", yytext);}
"<" {printf("%s - as operator\n", yytext);}
">" {printf("%s - as operator\n", yytext);}


[ \t]+  	{}

[\n]+	{++lineNumber;}

. {correct = 0; badLine = lineNumber; printf("Incorrect:%s\n", yytext);}


%%  
void main(int argc, char** argv)
{           
if (argc > 1)
{
    FILE *file;
    file = fopen(argv[1], "r");
    if (!file)
    {
        fprintf(stderr, "Could not open %s\n", argv[1]);
        exit(1);
    }
    yyin = file;
}

yylex();
if(correct == 1)
    printf("Correct program!");
else
    printf("Incorrect program at line %d!", badLine);
}