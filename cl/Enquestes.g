grammar Enquestes;
root : expr END EOF ;
text_token : CHAR
           | NUM
           ;

string : string text_token
       | text_token
       ;

pregunta : string PREG ;

expr_preg : ID ASSIG 'PREGUNTA' pregunta;

only_resp : NUM ASSIG string FIN;
respuestas : respuestas only_resp
           | only_resp;
expr_resp : ID ASSIG 'RESPOSTA' respuestas;

item : ID FLECHA ID ;
expr_item : ID ASSIG 'ITEM' item;

assoc : ABR_P NUM COMMA ID CRR_P ;
list_assoc : list_assoc COMMA assoc
           | assoc
           ;
alter : ID ABR_C list_assoc CRR_C ;

alter_expr : ID ASSIG 'ALTERNATIVA' alter;

encuesta : encuesta ID
         | ID
         ;
expr_enq : ID_E ASSIG 'ENQUESTA' encuesta ;

expr : expr expr
    | expr_enq
    | expr_preg
    | expr_resp
    | expr_item
    | alter_expr
    ;


COMMA : ',';
ABR_P : '(';
ABR_C : '[';
CRR_P : ')';
CRR_C : ']';
NUM : [0-9]+ ;
FLECHA : '->';
PREG : '?';
FIN : ';';
END : 'END';
ID_E: [A-Z]+?;
ID : [A-Z][0-9]+;
CHAR: [a-zA-Z\u0080-\u00FF]+ ;
ASSIG: ':';
NEWLINE:'\r'? '\n' -> skip ;
WS  :   (' '|'\t')+ -> skip ;