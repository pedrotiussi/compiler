from Scope.analyzer import *
from Semantic.analyzer import Semantic_Analysis
from syntatic.states import *
import os
from syntatic.table_action import TableAction


class SyntaticAnalysis:
    lexical = None
    syntaticalError = False

    def __init__(self, lexical):
        self.lexical = lexical
        self.table_action = TableAction()

    def parse(self):

        output_file_name = self.lexical.arq.name.split(".", maxsplit=1)[0] + ".txt"
        output_path = os.path.join("output", output_file_name)
        generated_code = open(output_path, "w")
        generated_code.close()

        STACK = []
        state = 0
        STACK.append(state)
        readToken = self.lexical.next_Token()
        # print(readToken)
        action = self.table_action.get_action(state + 1, readToken)
        # print(action)
        
        cont=0
        while action != "acc":
            self.lexical.Lexical_error(readToken)
            if self.lexical.lexicalError == True:
                break

            if action[0] == "s":
                state = int(action[1:])
                STACK.append(state)
                readToken = self.lexical.next_Token()
                action = self.table_action.get_action(state + 1, readToken)
                cont+=1
            
            elif action[0] == "r":
                rule = int(action[1:])
                for x in range(RIGHT[rule-1]):
                    STACK.pop()
                try:
                    state = int(self.table_action.get_action(STACK[-1]+1, LEFT[rule-1]))
                except:
                    print("Sintaxe Error in line "+str(self.lexical.line))
                    self.syntaticalError = True
                    break
                STACK.append(state)
                action = self.table_action.get_action(state + 1, readToken)
                cont+=1
                Semantic_Analysis(self.lexical, rule, output_path)
                
            else:
                self.syntaticalError = True
                print("Sintaxe Error in line " + str(self.lexical.line))
                break

