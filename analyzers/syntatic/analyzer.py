from analyzers.scope.analyzer import *
from analyzers.semantic.analyzer import SemanticAnalyzer
from analyzers.syntatic.states import *
import os
from analyzers.syntatic.table_action import TableAction


class SyntaticAnalyzer:
    syntaticalError = False

    def __init__(self, lexical):
        self.lexical = lexical
        self.table_action = TableAction()

    def parse(self):

        output_path = os.path.join("output", self.lexical.file_name)
        generated_code = open(output_path, "w")
        generated_code.close()

        STACK = []
        state = 0
        STACK.append(state)

        read_token = self.lexical.next_Token()
        action = self.table_action.get_action(state + 1, read_token)
        
        cont=0
        # acc: accept
        while action != "acc":
            self.lexical.Lexical_error(read_token)
            if self.lexical.lexicalError == True:
                break
            
            # s: state
            if action[0] == "s":
                state = int(action[1:])
                STACK.append(state)
                read_token = self.lexical.next_Token()
                action = self.table_action.get_action(state + 1, read_token)
                cont+=1
            
            # r: rule
            elif action[0] == "r":
                rule = int(action[1:])
                for x in range(RIGHT[rule-1]):
                    STACK.pop()

                try:
                    state = int(self.table_action.get_action(STACK[-1]+1, LEFT[rule-1]))

                except:
                    print("In line {self.lexical.line}: sintax error")
                    self.syntatic_error = True
                    break

                STACK.append(state)
                action = self.table_action.get_action(state + 1, read_token)
                SemanticAnalyzer(self.lexical, rule, output_path)
                cont+=1
                
            else:
                self.syntatic_error = True
                print(f"In line {self.lexical.line}: sintax error")
                break

