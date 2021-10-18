from analyzers.lexical.key_words import *
import string
import os


class LexicalAnalyzer:
    
    def __init__(self, file_path):
        self.file = open(file_path, 'r', encoding = 'utf-8')
        self.file.seek(0)
        self.file_name = os.path.basename(file_path)

        self.lexicalError = False
        self.next_char = " "
        self.v_ctes = []
        self.identifiers = {}
        self.count = 0
        self.secondary_Token = None
        self.line = 1
        self.ch = 1
        self.reserved_words = ["array", "boolean", "break", "char", "continue",
                               "do", "else", "false", "function", "if", "integer", 
                               "of", "string", "struct", "true", "type", "var", "while"
                              ]

    def search_reserved_word(self, word): 
        left = 0
        right = len(self.reserved_words) - 1
        while left <= right:
            middle = (left + right) // 2
            if self.reserved_words[middle] == word:
                return middle
            elif self.reserved_words[middle] > word:
                right = middle - 1
            else:
                left = middle + 1
        return ID

    def check_digit(self, c):
        return c in "0123456789"

    def check_alnum(self, c):
        return c in string.ascii_letters

    def check_space(self, c):
        return c in [chr(10), chr(13), "\f", "\v", "\t"," "]

    def add_cte(self, c):
        self.v_ctes.append(c)
        return len(self.v_ctes)-1

    def get_cte(self, c):
        return self.v_ctes[c]

    def search_name(self, name): 
        if name not in self.identifiers:
            self.identifiers[name] = self.count
            self.count += 1
        return self.identifiers[name]

    def next_token(self):
        sep = ""
        while self.check_space(self.next_char):
            if self.next_char == "\n" or self.next_char == "\r":
                self.line+=1
            self.next_char = self.file.read(1)
            self.ch+=1
        
        if self.next_char == "":
            token = EOF
        
        elif self.check_alnum(self.next_char):
            text_Aux = []
            while self.check_alnum(self.next_char) or self.next_char == '_':
                text_Aux.append(self.next_char)
                self.next_char = self.file.read(1)
                self.ch+=1
            word = sep.join(text_Aux)
            token = self.search_reserved_word(word)
            if token == ID:
                self.secondary_Token = self.search_name(word)
        
        elif self.check_digit(self.next_char):
            num_Aux = []
            while self.check_digit(self.next_char):
                num_Aux.append(self.next_char)
                self.next_char = self.file.read(1)
                self.ch+=1
            num = sep.join(num_Aux)
            token = NUMERAL
            self.secondary_Token = self.add_cte(num)
        
        elif self.next_char == "\"":
            string_Aux = []
            string_Aux.append(self.next_char)
            self.next_char = self.file.read(1)
            self.ch+=1
            if self.next_char != "\"":
                while(self.next_char!="\""):
                    string_Aux.append(self.next_char)
                    self.next_char = self.file.read(1)
                    self.ch+=1
            string_Aux.append(self.next_char)
            self.next_char = self.file.read(1)
            self.ch+=1
            string = sep.join(string_Aux)
            token = STRING
            self.secondary_Token = self.add_cte(string)
        
        else:
            if self.next_char == "\'":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = CHARACTER
                self.secondary_Token = self.add_cte(self.next_char)
                self.next_char = self.file.read(2) 
                self.ch+=2

            elif self.next_char == ":":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = COLON

            elif self.next_char == "+":
                self.next_char = self.file.read(1)
                self.ch+=1
                if self.next_char == "+":
                    token = PLUS_PLUS
                    self.next_char = self.file.read(1)
                    self.ch+=1
                else:
                    token = PLUS

            elif self.next_char == "-":
                self.next_char = self.file.read(1)
                self.ch+=1
                if self.next_char == "-":
                    token = MINUS_MINUS
                    self.next_char = self.file.read(1)
                    self.ch+=1
                else:
                    token = MINUS

            elif self.next_char == "*":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = TIMES

            elif self.next_char == ".":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = DOT        

            elif self.next_char == "/":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = DIVIDE

            elif self.next_char == "=":
                self.next_char = self.file.read(1)
                self.ch+=1
                if self.next_char == "=":
                    token = EQUAL_EQUAL
                    self.next_char = self.file.read(1)
                    self.ch+=1
                else:
                    token = EQUALS
            
            elif self.next_char == "!":
                self.next_char = self.file.read(1)
                self.ch+=1
                if self.next_char == "=":
                    token = NOT_EQUAL
                    self.next_char = self.file.read(1)
                    self.ch+=1
                else:
                    token = NOT 

            elif self.next_char == "<":
                self.next_char=self.file.read(1)
                self.ch+=1
                if self.next_char == "=":
                    token = LESS_OR_EQUAL
                    self.next_char = self.file.read(1)
                    self.ch+=1
                else:
                    token=LESS_THAN

            elif self.next_char == ">":
                self.next_char = self.file.read(1)
                self.ch+=1
                if self.next_char == "=":
                    token = GREATER_OR_EQUAL
                    self.next_char = self.file.read(1)
                    self.ch+=1
                else:
                    token = GREATER_THAN

            elif self.next_char == ";":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = SEMI_COLON

            elif self.next_char == ",":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = COMMA

            elif self.next_char == "[":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = LEFT_SQUARE

            elif self.next_char == "]":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = RIGHT_SQUARE

            elif self.next_char == "{":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = LEFT_BRACES

            elif self.next_char == "}":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = RIGHT_BRACES

            elif self.next_char == "(":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = LEFT_PARENTHESIS

            elif self.next_char == ")":
                self.next_char = self.file.read(1)
                self.ch+=1
                token = RIGHT_PARENTHESIS

            elif self.next_char == "&":
                self.next_char = self.file.read(1)
                self.ch+=1
                if self.next_char == "&":
                    self.next_char=self.file.read(1)
                    self.ch+=1
                    token = AND
                else:
                    token = UNKNOWN

            elif self.next_char == "|":
                self.next_char = self.file.read(1)
                self.ch+=1
                if self.next_char == "|":
                    self.next_char = self.file.read(1)
                    self.ch+=1
                    token = OR
                else:
                    token = UNKNOWN

            else:
                self.next_char = self.file.read(1)
                self.ch+=1
                token = UNKNOWN

        return token

    def lexical_error(self, token):
        if token == UNKNOWN:
            self.lexicalError = True
            print(f"Char {self.ch+1} not expected at line {self.line}")

    def run(self):
        self.next_char = self.file.read(1)
        token_Aux = self.next_token()
        while token_Aux != EOF:
            if token_Aux == UNKNOWN:
                print(f"Char {self.ch+1} not expected at line {self.line}")
                self.lexicalError = True
            token_Aux = self.next_token()
        if not self.lexicalError:
            print ("So far so good! None lexical errors on your code!\n")
        self.file.seek(0)
        self.next_char = " "

    def close_file(self):
        self.file.close()