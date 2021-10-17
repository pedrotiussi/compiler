from analyzers.lexical.analyzer import LexicalAnalyzer
from analyzers.syntatic.analyzer import SyntaticAnalyzer
import sys
import os

def run_compiler(input_file_path: str):

    lexical = LexicalAnalyzer(input_file_path)
    lexical.run()
    if lexical.lexicalError:
        exit()
    syntatical = SyntaticAnalyzer(lexical)
    syntatical.parse()


if __name__ == '__main__':
    try:
        test_file = sys.argv[1]
    except:
        test_file = os.path.join('input', 'test_code.txt')

    run_compiler(test_file)