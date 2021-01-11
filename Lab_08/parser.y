%{
#include <stdio.h>
#include <stdlib.h>

#define YYDEBUG 1
%}

%token IDENTIFIER
%token CONSTANT
%token MAIN
%token DEFINE
%token INTEGER
%token CHAR
%token WHILE
%token FOR
%token IF
%token ELSE
%token IN_INTEGER
%token IN_CHARS
%token OUT
%token PLUS
%token MINUS
%token MULTIPLY
%token DIVISION
%token MOD
%token IN_SIGN
%token LESS_OR_EQUAL_THAN
%token GREATER_OR_EQUAL_THAN
%token EQUAL
%token DIFFERENT
%token ASSIGNMENT
%token LESS_THAN
%token GREATER_THAN
%token LEFT_CURLY_PARENTHESIS
%token RIGHT_CURLY_PARENTHESIS
%token LEFT_SQUARE_PARENTHESIS
%token RIGHT_SQUARE_PARENTHESIS
%token LEFT_ROUND_PARENTHESIS
%token RIGHT_ROUND_PARENTHESIS
%token SEMI_COLON
%token COMMA


%start program

%%


program : MAIN LEFT_CURLY_PARENTHESIS declarationList stmtList RIGHT_CURLY_PARENTHESIS ;
declarationList : declaration | declaration declarationList ;
identifierList : IDENTIFIER SEMI_COLON | IDENTIFIER COMMA identifierList ;
declaration : DEFINE type identifierList;
type : mainTypes | arraysDecl ;
mainTypes : INTEGER | CHAR ;
arraysDecl : mainTypes LEFT_SQUARE_PARENTHESIS CONSTANT RIGHT_SQUARE_PARENTHESIS ;

vectorItem : IDENTIFIER LEFT_SQUARE_PARENTHESIS IDENTIFIER RIGHT_SQUARE_PARENTHESIS | IDENTIFIER LEFT_SQUARE_PARENTHESIS CONSTANT RIGHT_SQUARE_PARENTHESIS ;
item : IDENTIFIER | CONSTANT | vectorItem ;
operator : PLUS | MINUS | MULTIPLY | DIVISION | MOD ;
expression : item operator expression | item operator item | item | LEFT_ROUND_PARENTHESIS item operator expression RIGHT_ROUND_PARENTHESIS | LEFT_ROUND_PARENTHESIS item operator item RIGHT_ROUND_PARENTHESIS ;

RELATION : LESS_THAN | LESS_OR_EQUAL_THAN | EQUAL | DIFFERENT | GREATER_OR_EQUAL_THAN | GREATER_THAN ;

stmtList : stmt | stmt stmtList ;
stmt : assignStmt| inStmt | outStmt | ifStmt | whileStmt | forStmt ;
assignStmt : IDENTIFIER ASSIGNMENT expression SEMI_COLON | vectorItem ASSIGNMENT expression SEMI_COLON;
inStmt : IN_INTEGER IN_SIGN IDENTIFIER SEMI_COLON | IN_CHARS IN_SIGN IDENTIFIER SEMI_COLON | IN_CHARS IN_SIGN vectorItem SEMI_COLON | IN_INTEGER IN_SIGN vectorItem SEMI_COLON ;
outStmt : OUT LEFT_ROUND_PARENTHESIS CONSTANT RIGHT_ROUND_PARENTHESIS SEMI_COLON | OUT LEFT_ROUND_PARENTHESIS IDENTIFIER RIGHT_ROUND_PARENTHESIS SEMI_COLON; 
ifStmt : IF LEFT_ROUND_PARENTHESIS condition RIGHT_ROUND_PARENTHESIS LEFT_CURLY_PARENTHESIS stmtList RIGHT_CURLY_PARENTHESIS | IF LEFT_ROUND_PARENTHESIS condition RIGHT_ROUND_PARENTHESIS LEFT_CURLY_PARENTHESIS stmtList RIGHT_CURLY_PARENTHESIS ELSE LEFT_CURLY_PARENTHESIS stmtList RIGHT_CURLY_PARENTHESIS ;
whileStmt : WHILE LEFT_ROUND_PARENTHESIS condition RIGHT_ROUND_PARENTHESIS LEFT_CURLY_PARENTHESIS stmtList RIGHT_CURLY_PARENTHESIS ;
forStmt : FOR LEFT_ROUND_PARENTHESIS IDENTIFIER COMMA expression COMMA expression COMMA CONSTANT RIGHT_ROUND_PARENTHESIS LEFT_CURLY_PARENTHESIS stmtList RIGHT_CURLY_PARENTHESIS ;
condition : expression RELATION expression ;

%%

yyerror(char *s)
{
  printf("%s\n", s);
}

extern FILE *yyin;

main(int argc, char **argv)
{
  if (argc > 1) 
    yyin = fopen(argv[1], "r");
  if ( (argc > 2) && ( !strcmp(argv[2], "-d") ) ) 
    yydebug = 1;
  if ( !yyparse() ) 
    fprintf(stderr,"\t Good !!!\n");
}
