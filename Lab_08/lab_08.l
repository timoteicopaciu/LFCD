%{ 	 
    #include <stdio.h>
    #include "parser.tab.h"
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

"main" {printf( "%s - reserved word\n", yytext ); return MAIN; }
"define" {printf( "%s - reserved word\n", yytext ); return DEFINE;}
"Integer" {printf( "%s - reserved word\n", yytext ); return INTEGER;}
"Char" {printf( "%s - reserved word\n", yytext ); return CHAR;}
"while" {printf( "%s - reserved word\n", yytext ); return WHILE;}
"for" {printf( "%s - reserved word\n", yytext ); return FOR;}
"if" {printf( "%s - reserved word\n", yytext ); return IF;}
"else" {printf( "%s - reserved word\n", yytext ); return ELSE; }
"in.Integer" {printf( "%s - reserved word\n", yytext ); return IN_INTEGER;}
"in.Chars" {printf( "%s - reserved word\n", yytext ); return IN_CHARS;}
"out" {printf( "%s - reserved word\n", yytext ); return OUT;}

{identifier} {printf( "Identifier: %s\n", yytext ); return IDENTIFIER;}
{constant}	{printf( "Constant: %s\n", yytext ); return CONSTANT;}

"[" {printf("%s - as separator\n", yytext); return LEFT_SQUARE_PARENTHESIS;}
"]" {printf("%s - as separator\n", yytext); return RIGHT_SQUARE_PARENTHESIS; }
"{" {printf("%s - as separator\n", yytext); return LEFT_CURLY_PARENTHESIS; }
"}" {printf("%s - as separator\n", yytext); return RIGHT_CURLY_PARENTHESIS;}
"(" {printf("%s - as separator\n", yytext); return LEFT_ROUND_PARENTHESIS;}
")" {printf("%s - as separator\n", yytext); return RIGHT_ROUND_PARENTHESIS;}
";" {printf("%s - as separator\n", yytext); return SEMI_COLON;}
"," {printf("%s - as separator\n", yytext); return COMMA;}

"+" {printf("%s - as operator\n", yytext); return PLUS;}
"-" {printf("%s - as operator\n", yytext); return MINUS;}
"*" {printf("%s - as operator\n", yytext); return MULTIPLY;}
"/" {printf("%s - as operator\n", yytext);return DIVISION;}
"%" {printf("%s - as operator\n", yytext); return MOD;}
">>" {printf("%s - as operator\n", yytext); return IN_SIGN;}
"<=" {printf("%s - as operator\n", yytext); return LESS_OR_EQUAL_THAN; }
">=" {printf("%s - as operator\n", yytext); return GREATER_OR_EQUAL_THAN;}
"==" {printf("%s - as operator\n", yytext);return EQUAL;}
"!=" {printf("%s - as operator\n", yytext); return DIFFERENT;}
"=" {printf("%s - as operator\n", yytext); return ASSIGNMENT;}
"<" {printf("%s - as operator\n", yytext); return LESS_THAN;}
">" {printf("%s - as operator\n", yytext); return GREATER_THAN;}


[ \t]+  	{}

[\n]+	{++lineNumber;}

. {correct = 0; badLine = lineNumber; printf("Incorrect:%s\n", yytext);}


%%  