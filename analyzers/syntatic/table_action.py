from analyzers.syntatic.states import *
from analyzers.lexical.key_words import *
import csv


class TableAction:
    def __init__(self):
        self.TOKEN_TAB_ACTION = [
            INTEGER, CHAR, BOOLEAN, STRING, TYPE, EQUALS, ARRAY, LEFT_SQUARE,
            RIGHT_SQUARE, OF, STRUCT, LEFT_BRACES, RIGHT_BRACES, SEMI_COLON, 
            COLON, FUNCTION, LEFT_PARENTHESIS, RIGHT_PARENTHESIS, COMMA, VAR, 
            IF, ELSE, WHILE, DO, BREAK, CONTINUE, AND, OR, LESS_THAN, GREATER_THAN, 
            LESS_OR_EQUAL, GREATER_OR_EQUAL, EQUAL_EQUAL, NOT_EQUAL, PLUS, MINUS,
            TIMES, DIVIDE, PLUS_PLUS, MINUS_MINUS, NOT, DOT, ID, TRUE, FALSE,
            CHARACTER, STRINGVAL, NUMERAL, EOF, PLINHA, P, LDE, DE, T, DT, DC, 
            DF, LP, B, LDV, LS, DV, LI, S, U, M, E, L, R, Y, F, LE, LV, IDD, IDU,
            ID, TRUE, FALSE, CHR, STR, NUM, NB, MF, MC, NF, MT, ME, MW
        ]

        self.TAB_ACTION_GOTO = list(csv.reader(open("table_action.csv","r"), delimiter = "\t"))

    def token_table(self, a):
        return self.TOKEN_TAB_ACTION.index(a) + 1

    def get_action(self, state, token):
        action = self.TAB_ACTION_GOTO[state][self.token_table(token)]
        return action