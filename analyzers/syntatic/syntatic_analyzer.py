from analyzers.scope.scope_analyzer import *
from analyzers.lexical.lexical_analyzer import LexicalAnalyzer
from analyzers.semantic.semantic_analyzer import SemanticAnalyzer
from analyzers.syntatic.states import *
import os
from analyzers.syntatic.table_action import TableAction


class SyntaticAnalyzer:
    syntaticalError = False

    def __init__(self, lexical):
        self.lexical: LexicalAnalyzer = lexical
        self.table_action: TableAction = TableAction()

    def parse(self):

        output_path = os.path.join("output", self.lexical.file_name)
        generated_code = open(output_path, "w")
        generated_code.close()

        stack = []
        state = 0
        stack.append(state)
        read_token = self.lexical.next_token()
        action = self.table_action.get_action(state + 1, read_token) 
        cont=0

        # acc: accept the input as simple stack language code
        while action != "acc":
            self.lexical.lexical_error(read_token)
            if self.lexical.lexicalError == True:
                break
            
            # s*: some state
            if action[0] == "s":
                state = int(action[1:])
                stack.append(state)
                read_token = self.lexical.next_token()
                action = self.table_action.get_action(state + 1, read_token)
                cont+=1
            
            # r*: some rule
            elif action[0] == "r":
                rule = int(action[1:])
                for x in range(RIGHT[rule-1]):
                    stack.pop()

                try:
                    state = int(self.table_action.get_action(stack[-1]+1, LEFT[rule-1]))

                except:
                    print(f"Line {self.lexical.line}: sintax error")
                    self.syntatic_error = True
                    break

                stack.append(state)
                action = self.table_action.get_action(state + 1, read_token)
                SemanticAnalyzer(self.lexical, rule, output_path).analyze()
                cont+=1
                
            else:
                self.syntatic_error = True
                print(f"Line {self.lexical.line}: sintax error")
                break
            
            if action == 'acc':
                print("Well done! Syntatic OK!\n")
        
        
        print('This code is semantically right.\n')
        print(f'Code generated at output/{self.lexical.file_name}.\n')
        self.lexical.close_file()

