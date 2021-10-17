from analyzers.lexical.key_words import *
import string

# Key Words
key_words = ["array", "boolean", "break", "char", "continue",
             "do", "else", "false", "function", "if", "integer", 
             "of", "string", "struct", "true", "type", "var", "while"]

class LexicalAnalyzer:
    lexicalError = False
    next_char = " "
    arq = None

    def __init__(self, file):
        file.seek(0)
        self.arq = file

    def search_Key_Word(self, name): 
        left = 0
        right = len(key_words) - 1
        while left <= right:
            middle = (left + right) // 2
            if key_words[middle] == name:
                return middle
            elif key_words[middle] > name:
                right = middle - 1
            else:
                left = middle + 1
        return ID

    # Literals
    v_Ctes = []

    def add_Cte(self, c):
        self.v_Ctes.append(c)
        return len(self.v_Ctes)-1

    def get_Cte(self, c):
        return self.v_Ctes[c]

    # Identifiers
    identifiers = {}
    count = 0

    def search_Name(self, name): 
        if name not in self.identifiers:
            self.identifiers[name] = self.count
            self.count += 1
        return self.identifiers[name]

    secondary_Token = None
    line = 1
    ch = 1

    def next_Token(self):
        sep = ""
        while self.check_space(self.next_char):
            if self.next_char == "\n" or self.next_char == "\r":
                self.line+=1
            self.next_char = self.arq.read(1)
            self.ch+=1
        
        if self.next_char == "":
            token = EOF
        
        elif self.check_alnum(self.next_char):
            text_Aux = []
            while self.check_alnum(self.next_char) or self.next_char == '_':
                text_Aux.append(self.next_char)
                self.next_char = self.arq.read(1)
                self.ch+=1
            text = sep.join(text_Aux)
            token = self.search_Key_Word(text)
            if token == ID:
                self.secondary_Token = self.search_Name(text)
        
        elif self.check_digit(self.next_char):
            num_Aux = []
            while self.check_digit(self.next_char):
                num_Aux.append(self.next_char)
                self.next_char = self.arq.read(1)
                self.ch+=1
            num = sep.join(num_Aux)
            token = NUMERAL
            self.secondary_Token = self.add_Cte(num)
        
        elif self.next_char == "\"":
            string_Aux = []
            string_Aux.append(self.next_char)
            self.next_char = self.arq.read(1)
            self.ch+=1
            if self.next_char != "\"":
                while(self.next_char!="\""):
                    string_Aux.append(self.next_char)
                    self.next_char = self.arq.read(1)
                    self.ch+=1
            string_Aux.append(self.next_char)
            self.next_char = self.arq.read(1)
            self.ch+=1
            string = sep.join(string_Aux)
            token = STRING
            self.secondary_Token = self.add_Cte(string)
        
        else:
            if self.next_char == "\'":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = CHARACTER
                self.secondary_Token = self.add_Cte(self.next_char)
                self.next_char = self.arq.read(2) 
                self.ch+=2

            elif self.next_char == ":":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = COLON

            elif self.next_char == "+":
                self.next_char = self.arq.read(1)
                self.ch+=1
                if self.next_char == "+":
                    token = PLUS_PLUS
                    self.next_char = self.arq.read(1)
                    self.ch+=1
                else:
                    token = PLUS

            elif self.next_char == "-":
                self.next_char = self.arq.read(1)
                self.ch+=1
                if self.next_char == "-":
                    token = MINUS_MINUS
                    self.next_char = self.arq.read(1)
                    self.ch+=1
                else:
                    token = MINUS

            elif self.next_char == "*":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = TIMES

            elif self.next_char == ".":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = DOT        

            elif self.next_char == "/":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = DIVIDE

            elif self.next_char == "=":
                self.next_char = self.arq.read(1)
                self.ch+=1
                if self.next_char == "=":
                    token = EQUAL_EQUAL
                    self.next_char = self.arq.read(1)
                    self.ch+=1
                else:
                    token = EQUALS
            
            elif self.next_char == "!":
                self.next_char = self.arq.read(1)
                self.ch+=1
                if self.next_char == "=":
                    token = NOT_EQUAL
                    self.next_char = self.arq.read(1)
                    self.ch+=1
                else:
                    token = NOT 

            elif self.next_char == "<":
                self.next_char=self.arq.read(1)
                self.ch+=1
                if self.next_char == "=":
                    token = LESS_OR_EQUAL
                    self.next_char = self.arq.read(1)
                    self.ch+=1
                else:
                    token=LESS_THAN

            elif self.next_char == ">":
                self.next_char = self.arq.read(1)
                self.ch+=1
                if self.next_char == "=":
                    token = GREATER_OR_EQUAL
                    self.next_char = self.arq.read(1)
                    self.ch+=1
                else:
                    token = GREATER_THAN

            elif self.next_char == ";":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = SEMI_COLON

            elif self.next_char == ",":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = COMMA

            elif self.next_char == "[":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = LEFT_SQUARE

            elif self.next_char == "]":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = RIGHT_SQUARE

            elif self.next_char == "{":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = LEFT_BRACES

            elif self.next_char == "}":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = RIGHT_BRACES

            elif self.next_char == "(":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = LEFT_PARENTHESIS

            elif self.next_char == ")":
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = RIGHT_PARENTHESIS

            elif self.next_char == "&":
                self.next_char = self.arq.read(1)
                self.ch+=1
                if self.next_char == "&":
                    self.next_char=self.arq.read(1)
                    self.ch+=1
                    token = AND
                else:
                    token = UNKNOWN

            elif self.next_char == "|":
                self.next_char = self.arq.read(1)
                self.ch+=1
                if self.next_char == "|":
                    self.next_char = self.arq.read(1)
                    self.ch+=1
                    token = OR
                else:
                    token = UNKNOWN

            else:
                self.next_char = self.arq.read(1)
                self.ch+=1
                token = UNKNOWN

        return token

    def Lexical_error(self, token):
        if token == UNKNOWN:
            self.lexicalError = True
            print(f"In the line {self.line}: character {self.ch+1} not expected")

    def run(self):
        self.next_char = self.arq.read(1)
        token_Aux = self.next_Token()
        while token_Aux != EOF:
            if token_Aux == UNKNOWN:
                print(f"In the line {self.line}: character {self.ch+1} not expected")
                self.lexicalError = True
            token_Aux = self.next_Token()
        if not self.lexicalError:
            print ("No lexical errors.")

    def check_digit(self, c):
        if c in "0123456789":
            return True
        return False

    def check_alnum(self, c):
        if c in string.ascii_letters:
            return True
        return False

    def check_space(self, c):
        if c in [chr(10), chr(13), "\f", "\v", "\t"," "]:
            return True
        return False
